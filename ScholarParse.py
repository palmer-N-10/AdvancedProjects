import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_main_list(url):
    # Scrapes a single scholarship listing page for:
    #   - Award
    #   - Deadline
    #   - Name
    #   - Scholarship Link (details page)
    #   - Description
    #   - More Info Link
    # Returns a list of dictionaries, each representing one scholarship item.
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    scholarship_rows = soup.find_all("div", class_="row")

    scraped_data = []
    for row in scholarship_rows:
        summary_div = row.find("div", class_="scholarship-summary")
        if not summary_div:
            continue

        # Award
        award_span = summary_div.find("span", class_="lead")
        award = award_span.get_text(strip=True) if award_span else None

        # Deadline
        all_paragraphs = summary_div.find_all("p")
        deadline = None
        if len(all_paragraphs) > 1:
            deadline_strong = all_paragraphs[1].find("strong")
            if deadline_strong:
                deadline = deadline_strong.get_text(strip=True)

        # "More info" link
        more_info_a = summary_div.find("a", text="More info")
        more_info_link = more_info_a["href"] if more_info_a else None

        # Scholarship description
        desc_div = row.find("div", class_="scholarship-description")
        if not desc_div:
            continue

        name_h4 = desc_div.find("h4")
        if name_h4 and name_h4.find("a"):
            scholarship_name = name_h4.find("a").get_text(strip=True)
            scholarship_link = name_h4.find("a")["href"]
        else:
            scholarship_name = None
            scholarship_link = None

        desc_paragraphs = desc_div.find_all("p")
        scholarship_description = ""
        if len(desc_paragraphs) > 1:
            scholarship_description = desc_paragraphs[1].get_text(strip=True)

        scholarship_data = {
            "Name": scholarship_name,
            "Scholarship Link": scholarship_link,  
            "Award": award,
            "Deadline": deadline,
            "Description": scholarship_description,
            "More Info Link": more_info_link
        }
        scraped_data.append(scholarship_data)

    return scraped_data


def scrape_sponsor_info(detail_url):

    # Visits the scholarship's detail page to scrape sponsor information:
    #   - Sponsor Name
    #   - Sponsor Address
    #   - Sponsor Phone
    #   - Sponsor Website
    # Returns a dictionary with these fields (or None/empty if missing).

    if not detail_url:
        return {
            "Sponsor Name": None,
            "Sponsor Address": None,
            "Sponsor Phone": None,
            "Sponsor Website": None
        }

    resp = requests.get(detail_url)
    if resp.status_code != 200:
        print(f"Failed to retrieve detail page {detail_url}. Status code: {resp.status_code}")
        return {
            "Sponsor Name": None,
            "Sponsor Address": None,
            "Sponsor Phone": None,
            "Sponsor Website": None
        }

    detail_soup = BeautifulSoup(resp.text, "html.parser")
    sponsor_div = detail_soup.find("div", class_="sponsor")
    if not sponsor_div:
        return {
            "Sponsor Name": None,
            "Sponsor Address": None,
            "Sponsor Phone": None,
            "Sponsor Website": None
        }

    sponsor_p = sponsor_div.find("p")
    if not sponsor_p:
        return {
            "Sponsor Name": None,
            "Sponsor Address": None,
            "Sponsor Phone": None,
            "Sponsor Website": None
        }

    sponsor_text = sponsor_p.get_text("\n", strip=True)
    lines = sponsor_text.split("\n")

    sponsor_name_el = sponsor_p.find("strong")
    sponsor_name = sponsor_name_el.get_text(strip=True) if sponsor_name_el else None

    # Find phone
    sponsor_phone = None
    for line in lines:
        if line.lower().startswith("phone:"):
            sponsor_phone = line.split(":", 1)[-1].strip()
            break

    # Sponsor website
    sponsor_a = sponsor_p.find("a")
    sponsor_website = sponsor_a["href"] if sponsor_a else None

    # Naive approach: assume address is in the second line
    sponsor_address = None
    if len(lines) > 1:
        second_line = lines[1].strip()
        if not second_line.lower().startswith("phone:"):
            sponsor_address = second_line

    return {
        "Sponsor Name": sponsor_name,
        "Sponsor Address": sponsor_address,
        "Sponsor Phone": sponsor_phone,
        "Sponsor Website": sponsor_website
    }


if __name__ == "__main__":
    base_url_template = "https://www.collegescholarships.org/financial-aid/?page={}"
    all_scholarships = []

    # Loop through all pages
    for page_num in range(1, 770):
        url = base_url_template.format(page_num)
        print(f"Scraping main listing: {url}")
        main_page_scholarships = scrape_main_list(url)

        # For each scholarship, scrape the sponsor info
        for scholarship_data in main_page_scholarships:
            detail_link = scholarship_data["Scholarship Link"]
            if detail_link:
                sponsor_data = scrape_sponsor_info(detail_link)
                scholarship_data.update(sponsor_data)

                # OPTIONAL: Add a short delay to be polite. will take much longer to run if you do
                # time.sleep(1)

        # Accumulate all results in one master list
        all_scholarships.extend(main_page_scholarships)
        if page_num %50==0:
            print(page_num)
        # You might also add a delay between pages:
        time.sleep(1)

    # Finally, save to Excel
    df = pd.DataFrame(all_scholarships)
    output_file = "scholarships_all_pages_with_sponsors.xlsx"
    df.to_excel(output_file, index=False)

    print(f"\nDone! Scraped pages 1–769.\nTotal scholarships scraped: {len(all_scholarships)}\nData saved to '{output_file}'.")
