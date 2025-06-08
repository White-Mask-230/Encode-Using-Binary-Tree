"""
    Module implementing a prime-factorization-based encoding and decoding system.

    This module generates a hierarchical encoding dictionary mapping unique symbols from 
    input text to distinct composite integers formed by products of prime numbers arranged 
    in layers. Each layer corresponds to an exponential expansion of symbols encoded with 
    unique prime factors ensuring collision-free reversible mappings.

    Functionality includes:
        * Dynamically generating a sufficient set of prime numbers tailored to input size.
        * Incremental serialization of dictionaries and encoded text to disk for memory efficiency.
        * Public API exposing creation of encoding/decoding dictionaries, text encoding, and decoding.
        * Support for full ASCII range including alphabetic characters, digits, and special symbols.

    This design facilitates reversible and scalable symbol encoding suitable for custom 
    lightweight cryptographic or compression applications.
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

def create_dictionary_of_keys(text: List[str]) -> Tuple[str, str]:
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

def decode(encoded_path: str, inverted_dict_path: str) -> List[str]:
    """
        Decodes an encoded text file using an inverted dictionary stored in a file,
        reading both files line by line to minimize memory usage.

        Args:
            encoded_path (str): Path to the encoded text file.
            inverted_dict_path (str): Path to the inverted dictionary JSON file.

        Returns:
            List[str]: The decoded text as a list of strings.
    """

    code_to_symbol = {}

    with open(inverted_dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            code_to_symbol.update(d)

    decoded_lines = []

    with open(encoded_path, 'r', encoding='utf-8') as encoded_file:
        for line in encoded_file:
            line = line.strip()

            if not line:
                decoded_lines.append('')
                continue

            codes = line.split(',')
            decoded_line = []

            for code in codes:
                symbol = code_to_symbol.get(code, '')
                decoded_line.append(symbol)

            decoded_lines.append(''.join(decoded_line))

    print(f"[INFO] Decoded text loaded from: {encoded_path}")

    return decoded_lines

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
        decoded = decode(encoded_file, inverted_path)

        if decoded == case:
            print("[RESULT] OK")
        else:
            print("[RESULT] FAIL")
            print("Expected:", case)
            print("Received:", decoded)

if __name__ == '__main__':
    _test()
