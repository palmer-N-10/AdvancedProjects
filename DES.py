# This table is used to permute the 64-bit input key into a 56-bit key 
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# This table is used to permute the 56-bit key halves (C and D) into a 48-bit round key
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]


# Shift schedule for the 16 rounds of DES (1-bit shift for round 1)
# This array contains the number of left shifts to be applied to the key halves (C and D) in each round
SHIFT_SCHEDULE = [1] * 16

# Convert hex string to binary string
def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(64)

# Permutation function
# Reorders the bits in a block according to a given table
def permute(block, table):
    return ''.join(block[i - 1] for i in table)

##Q1##
# Step 1: Derive the Round 1 key (K1) by reducing the 64-bit key to 56 bits using PC-1
def derive_round_1_key(initial_key):
    # Convert the initial key from hexadecimal (64-bit) to binary
    initial_key_bin = hex_to_bin(initial_key)
    initial_key_bin_spaced = ' '.join(initial_key_bin[i:i+4] for i in range(0, len(initial_key_bin), 4))
    print(f" 1a: Initial 64-bit Key in Binary: {initial_key_bin_spaced}")

    # Apply PC-1 permutation to reduce the 64-bit key to 56 bits
    permuted_key = permute(initial_key_bin, PC1)
    permuted_key_spaced = ' '.join(permuted_key[i:i+4] for i in range(0, len(permuted_key), 4))
    print(f"56-bit Key PC-1: {permuted_key_spaced}")

    # Split the 56-bit permuted key into two 28-bit halves (C0 and D0)
    C0, D0 = permuted_key[:28], permuted_key[28:]
    C0_spaced = ' '.join(C0[i:i+4] for i in range(0, len(C0), 4))
    D0_spaced = ' '.join(D0[i:i+4] for i in range(0, len(D0), 4))
    print(f"1b: C0 (28-bit Left Half): {C0_spaced}")
    print(f"D0 (28-bit Right Half): {D0_spaced}")
    # Return the initial key halves (C0 and D0)
    return C0, D0

# Circular left shift function for key halves (C and D)
# Shifts the bits of the input by a given amount (shift_amount) in a circular fashion.
def left_shift(bits, shift_amount):
    return bits[shift_amount:] + bits[:shift_amount]

# Step 2: Derive the Round 1 subkey (K1) by shifting the key halves and applying PC-2
def derive_round_1_subkey(C0, D0):
    # Perform a 1-bit left shift on both C0 and D0 as per the shift schedule
    C1 = left_shift(C0, SHIFT_SCHEDULE[0])
    D1 = left_shift(D0, SHIFT_SCHEDULE[0])
    
    # Format C1 and D1 for display by adding spaces between every 4 bits
    C1_spaced = ' '.join(C1[i:i+4] for i in range(0, len(C1), 4))
    D1_spaced = ' '.join(D1[i:i+4] for i in range(0, len(D1), 4))
    print(f"1c: C1 after left shift: {C1_spaced}")
    print(f"D1 after left shift: {D1_spaced}")

    # Combine the shifted halves (C1 and D1) to create a 56-bit key
    combined_key = C1 + D1
    combined_key_spaced = ' '.join(combined_key[i:i+4] for i in range(0, len(combined_key), 4))
    print(f"Combined C1 and D1: {combined_key_spaced}")
    
    # Apply PC-2 to generate the 48-bit round key K1
    K1 = permute(combined_key, PC2)
    K1_space = ' '.join(K1[i:i+4] for i in range(0, len(K1), 4))
    print(f"48-bit Round (K1) PC-2: {K1_space}")
    
    # Return the 48-bit round key (K1)
    return K1

##Q2##
# Initial Permutation table
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Expansion Permutation table
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation table
P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# S-box 1 
S1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

# S-box 2 
S2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
]

# S-box 3 
S3 = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
]

# S-box 4 
S4 = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
]

# S-box 5 
S5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
]

# S-box 6
S6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
]

# S-box 7 
S7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
]

# S-box 8 
S8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

# Function to apply permutation P to a 32-bit block
def permutation_P(B):
    return permute(B, P)

def initial_permutation(plaintext_bin):
    return permute(plaintext_bin, IP)

def text_to_bin(plaintext):
    binary_text = ''.join(format(ord(char), '08b') for char in plaintext)
    return binary_text

# Expansion function to expand 32-bit R0 to 48 bits
def expansion(R0):
    return permute(R0, E)

# XOR function to perform bitwise XOR between two binary strings
def xor(bin1, bin2):
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bin1, bin2))

# Function to apply S-box substitutions
def s_box_substitution(A):
    # Split A into eight 6-bit blocks
    blocks = [A[i:i+6] for i in range(0, len(A), 6)]
    
    result = ''
    S_boxes = [S1, S2, S3, S4, S5, S6, S7, S8]  # Now includes all eight S-boxes
    
    for i, block in enumerate(blocks):
        # Apply the S-box substitution for the ith block
        # Extract row (first and last bits) and column (middle 4 bits)
        row = int(block[0] + block[-1], 2)  # First and last bits for row
        col = int(block[1:5], 2)            # Middle 4 bits for column
        
        # Substitute using the ith S-box (S1, S2, ..., S8)
        s_value = S_boxes[i][row][col]
        result += format(s_value, '04b')  # Convert to 4-bit binary string
    
    return result

    
# Helper function to add spaces every 4 characters in a binary string
def format_binary_with_spaces(binary_string):
    return ' '.join(binary_string[i:i+4] for i in range(0, len(binary_string), 4))

def round_1_encryption(plaintext, K1):
    # Step 1: Convert the plaintext into binary
    plaintext_bin = text_to_bin(plaintext)
    print(f"2a: Plaintext in Binary: {format_binary_with_spaces(plaintext_bin)}")

    # Step 2: Apply the initial permutation (IP) and split into L0 and R0
    permuted_text = initial_permutation(plaintext_bin)
    L0, R0 = permuted_text[:32], permuted_text[32:]
    print(f"2b: L0: {format_binary_with_spaces(L0)}")
    print(f"R0: {format_binary_with_spaces(R0)}")

    # Step 3: Expand R0 to 48 bits using the expansion function
    expanded_R0 = expansion(R0)
    print(f"2c: E(R0): {format_binary_with_spaces(expanded_R0)}")

    # Step 4: Calculate A = E(R0) ^xor K1
    A = xor(expanded_R0, K1)
    print(f"2d: A = E(R0) ^ K1: {format_binary_with_spaces(A)}")

    # Step 5: Group A into sets of 6 bits
    blocks = [A[i:i+6] for i in range(0, len(A), 6)]
    print("2e: A grouped into sets of 6 bits:")
    for idx, block in enumerate(blocks):
        print(f"Block {idx+1}: {block}")

    # Step 5.1 continued: Apply the S-box substitution
    B = s_box_substitution(A)
    print(f"2f: S-box result (32-bit B): {format_binary_with_spaces(B)}")

    # Step 6: Apply permutation P to the 32-bit result B
    P_B = permutation_P(B)
    print(f"2g: P(B): {format_binary_with_spaces(P_B)}")

    # Step 7: Calculate R1 = P(B) ^xor L0
    R1 = xor(P_B, L0)
    print(f"2h: R1: {format_binary_with_spaces(R1)}")

    # The result for this round is L1 = R0 and R1
    L1 = R0
    print(f"L1: {format_binary_with_spaces(L1)}")
    print(f"Final result after round 1: L1 = {format_binary_with_spaces(L1)}, R1 = {format_binary_with_spaces(R1)}")

initial_key = '0123456789ABCDEF'

# Call the function to derive the round 1 key
C0, D0 = derive_round_1_key(initial_key)

# Derive the round 1 subkey (K1) 
K1 = derive_round_1_subkey(C0, D0)
print('----------------------------------------------------------------')
round_1_encryption("MESSAGES", K1)