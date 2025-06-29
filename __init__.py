"""
# General script information
* Description: Encryption using prime numbers and binary tree structure.
* Creator: Lucas Varela Correa
* Version: 1.0.0
* Creation date: 06/29/2025

# Included functions
* create_dictionary_of_keys
* encode
* decode
For more information about their arguments or how they work, please visit the function of your interest.

* Requirements:
    - Python version > 3.5

# Script usage
This script has been designed to be used as a library. An example script is shown below so you can start using this library right away:
import EUBTA

cases = [
    ['hello my name is kopo', 'hello kopo'],
    ['IOPOI PODI', 'DI'],
    ['12 34 19', '98 09 12 13'],
    ['////?????? ####,,,,....======'],
    ['Ho mo lo 123-123-234-55', 'Po om pol #pom', '1 + 2 = 3']
]

for i, case in enumerate(cases):
    dict_path, inverted_path = create_dictionary_of_keys(case)
    encoded_file = encode(case, dict_path)
    decoded_file = decode(encoded_file, inverted_path)

    print(f'Your dict path: {dict_path}')
    print(f'Your inverted path: {inverted_path}')
    print(f'Your encoded file path: {encoded_file}')
    print(f'Your decoded file path: {decoded_file}')

# License
This project uses the MIT License. For more information, please visit: https://github.com/White-Mask-230/Encode-Using-Binary-Tree/blob/main/LICENSE

# Legal Notice
This script is provided "as is", without any warranties of any kind. It was created and shared for educational and research purposes only. Misuse of this script may be illegal in some jurisdictions.
Make sure to comply with all applicable laws and regulations when using this script. The creator is not responsible for any damage or issues that may arise from its use.

# Social Media
* GitHub: https://github.com/White-Mask-230
* Twitter (X): https://x.com/LucasVarelaCor1
"""

import random, json
from typing import List, Tuple

__all__ = ['create_dictionary_of_keys', 'encode', 'decode']
__author__ = 'White Mask 230 (Lucas Varela Correa)'

def _generate_prime_numbers(n: int) -> List[int]:
    """
        Generate at least `n` prime numbers.

        This function uses a simple method to generate prime numbers by checking divisibility.

        Args:
            n (int): The number of prime numbers to generate.

        Returns:
            List[int]: A list containing at least `n` prime numbers.
    """

    primes = []
    candidate = 2

    while len(primes) < n:
        is_prime = True
        limit = int(candidate**0.5) + 1

        for i in range(2, limit):
            if candidate % i == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)

        candidate += 1

    return primes

def create_dictionary_of_keys(text: List[str], dict_file_path="dictionary.json", inverted_file_path="inverted_dictionary.json") -> Tuple[str, str]:
    """
        Creates encoding and decoding dictionaries from the given text and saves them to files.

        The dictionaries are written incrementally to files layer by layer to avoid
        excessive memory usage. The encoding dictionary maps symbols to unique numeric codes,
        and the decoding dictionary is the inverse.

        Args:
            text (List[str]): A list of strings representing the text to encode.

        Returns:
            Tuple[str, str]: Tuple containing paths to the encoding dictionary file and the
                            decoding (inverted) dictionary file.
    """

    all_text = ''.join(text)
    symbols = sorted(set(all_text))

    required_primes = len(symbols) * 4
    primes = _generate_prime_numbers(required_primes)
    random.shuffle(primes)

    dict_file_path = "dictionary.json"
    inverted_file_path = "inverted_dictionary.json"

    with open(dict_file_path, 'w', encoding='utf-8') as dict_file, \
         open(inverted_file_path, 'w', encoding='utf-8') as inverted_file:

        dictionary_of_keys = {}
        inverted_dict = {}

        index = 0
        layer = 0
        total_symbols = len(symbols)

        while index < total_symbols:
            layer_key = f"layer {layer}"
            dictionary_of_keys[layer_key] = {}

            elements_in_layer = 2 ** layer

            for local_index in range(elements_in_layer):
                if index >= total_symbols:
                    break

                symbol = symbols[index]

                if layer == 0:
                    base = 1
                else:
                    prev_layer_key = f"layer {layer - 1}"
                    prev_values = list(dictionary_of_keys[prev_layer_key].values())
                    base_index = local_index // 2
                    if base_index >= len(prev_values):
                        base_index = len(prev_values) - 1
                    base = prev_values[base_index]

                prime = primes.pop()
                code = base * prime

                while code in inverted_dict:
                    if not primes:
                        raise ValueError("Ran out of prime numbers to assign codes.")

                    prime = primes.pop()
                    code = base * prime

                dictionary_of_keys[layer_key][symbol] = code
                inverted_dict[str(code)] = symbol

                index += 1

            dict_file.write(json.dumps({layer_key: dictionary_of_keys[layer_key]}) + "\n")
            dict_file.flush()

            layer += 1

        for code, symbol in inverted_dict.items():
            inverted_file.write(json.dumps({code: symbol}) + "\n")

        inverted_file.flush()

    print(f"[INFO] Encoding dictionary saved to: {dict_file_path}")
    print(f"[INFO] Decoding dictionary saved to: {inverted_file_path}")

    return dict_file_path, inverted_file_path

def encode(text: List[str], dict_path: str) -> str:
    """
        Encodes a list of strings using a dictionary stored in a file, avoiding loading
        the entire dictionary into memory at once.

        Args:
            text (List[str]): The original text to encode.
            dict_path (str): Path to the JSON dictionary file generated by `create_dictionary_of_keys`.

        Returns:
            str: Path to the file where the encoded text is saved.
    """

    symbol_to_code = {}

    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            layer_dict = json.loads(line)

            for layer in layer_dict.values():
                symbol_to_code.update(layer)

    encoded_file_path = "encoded_text.txt"
    with open(encoded_file_path, 'w', encoding='utf-8') as encoded_file:
        for line in text:
            encoded_line = []

            for ch in line:
                code = symbol_to_code.get(ch)

                if code is not None:
                    encoded_line.append(str(code))
                else:
                    encoded_line.append(ch)

            encoded_file.write(','.join(encoded_line) + "\n")

    print(f"[INFO] Encoded text saved to: {encoded_file_path}")

    return encoded_file_path

def decode(encoded_path: str, inverted_dict_path: str) -> None:
    """
        Decode the encoded file line by line using an inverted dictionary file,
        and write each decoded line immediately to an output text file to minimize memory usage.

        Args:
            encoded_path (str): Path to the encoded text file.
            inverted_dict_path (str): Path to the inverted dictionary JSON file.
            output_path (str): Path to the output file to save decoded text.
    """
    output_path = "decode.txt"

    code_to_symbol = {}

    with open(inverted_dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            code_to_symbol.update(d)

    with open(encoded_path, 'r', encoding='utf-8') as encoded_file, \
         open(output_path, 'w', encoding='utf-8') as output_file:
        
        for line in encoded_file:
            line = line.strip()

            if not line:
                output_file.write('\n')
                continue

            decoded_line = ''.join(code_to_symbol.get(code, '') for code in line.split(','))

            output_file.write(decoded_line + '\n')

    print(f"[INFO] Decoded text written to: {output_path}")

    return output_path

def _test():
    """
        Internal test routine for encoding and decoding.
        Prints results and cleans up temporary files.
    """

    cases = [
        ['hello my name is kopo', 'hello kopo'],
        ['IOPOI PODI', 'DI'],
        ['12 34 19', '98 09 12 13'],
        ['////?????? ####,,,,....======'],
        ['Ho mo lo 123-123-234-55', 'Po om pol #pom', '1 + 2 = 3']
    ]

    for i, case in enumerate(cases):
        print(f"\n[TEST] Case {i + 1}")

        dict_path, inverted_path = create_dictionary_of_keys(case)
        encoded_file = encode(case, dict_path)

        decoded_output_path = decode(encoded_file, inverted_path)

        with open(decoded_output_path, 'r', encoding='utf-8') as f:
            decoded = [line.rstrip('\n') for line in f]

        if decoded == case:
            print("[RESULT] OK")
        else:
            print("[RESULT] FAIL")
            print("Expected:", case)
            print("Received:", decoded)

if __name__ == '__main__':
    _test()
