
DES.py

Description

DES.py provides an illustrative step-by-step partial implementation of the Data Encryption Standard (DES). It focuses on showing how to generate the first round key (K1) and how to process the first round of the DES encryption algorithm on a given plaintext.

Key functionalities

Key Preparation: Converts a 64-bit hexadecimal key into binary, applies the PC-1 permutation, and splits it into two 28-bit halves.
Round Key Generation: Shifts the halves according to a schedule, applies the PC-2 permutation to form a 48-bit subkey (K1).
Initial Permutation: Permutes the 64-bit plaintext using the standard initial permutation (IP).
Expansion & S-Boxes: Expands the right half to 48 bits, XORs with the subkey, then uses S-boxes for substitution and permutation (P).
Round Function: Demonstrates how the left and right halves are swapped for the next round.


ImageNetLayerExploration.ipynb

Description

This Jupyter notebook (exact contents are not shown in this conversation, but presumably) explores various layers of a deep learning model trained on ImageNet. It might contain visualizations of activations, code snippets for loading images and running them through a CNN, or analysis of feature maps.


Neural Network Layer Visualization: Examines or visualizes the output of certain layers in a CNN.
Feature Extraction: Possibly uses a pre-trained network (e.g., a ResNet or VGG) to extract features from ImageNet images.
Layer-by-Layer Analysis: Observes changes in activation maps, layer outputs, or classification probabilities.

ScholarParse.py

Description

ScholarParse.py is a Python script that scrapes scholarship information from a website (e.g. collegescholarships.org). It uses the requests library to fetch the pages and BeautifulSoup (from bs4) to parse HTML content. It compiles data about scholarships into a DataFrame and saves it to an Excel file.

Key functionalities

Scrape Main List: Gathers scholarship data (award amount, deadline, name, links) from multiple pages.
Scrape Sponsor Info: Extracts additional sponsor information from each scholarship’s detail page.
Save to Excel: Stores everything in a single Excel file with all scraped fields.
