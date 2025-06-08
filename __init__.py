#TODO hacer que la generación de archivos sea automatica
#TODO crear una función main para ejecutar el programa normal
#TODO pasar la documentación a ingles
#TODO generar un documento tecnico y publicarlo en alguna revista

import random
import json
from typing import Tuple, List

__author__ = 'White Mask 230 (Lucas Varela Correa)'


def generate_prime_numbers(limit: int = 300) -> List[int]:
    """Genera una lista de números primos hasta un límite dado."""
    primes = []
    for num in range(2, limit):
        if all(num % div != 0 for div in range(2, int(num ** 0.5) + 1)):
            primes.append(num)
    return primes


def create_dictionary_of_keys(text: List[str]) -> Tuple[dict, dict]:
    """
    Crea un diccionario de codificación basado en capas usando números primos.

    Args:
        text (List[str]): Lista de líneas de texto a codificar.

    Returns:
        Tuple[dict, dict]: (Diccionario de codificación, Diccionario invertido de decodificación)
    """
    full_text = ''.join(text)
    symbols = sorted(set(full_text))  # Incluye todos los símbolos, números y letras

    primes = generate_prime_numbers()
    random.shuffle(primes)

    dictionary_of_keys = {}
    inverted_dict = {}
    used_values = set()

    layer = 0
    index = 0

    total_symbols = len(symbols)

    while index < total_symbols:
        key = f"layer {layer}"
        dictionary_of_keys[key] = {}

        elements_in_layer = 2 ** layer
        for local_index in range(elements_in_layer):
            if index >= total_symbols:
                break

            symbol = symbols[index]
            if layer == 0:
                base = 1
            else:
                # Accede de forma segura al valor base en la capa anterior
                previous_layer_values = list(dictionary_of_keys[f"layer {layer - 1}"].values())
                base_index = local_index // 2
                if base_index >= len(previous_layer_values):
                    base_index = len(previous_layer_values) - 1
                base = previous_layer_values[base_index]

            if not primes:
                raise ValueError("No hay suficientes números primos para generar los códigos.")

            prime = primes.pop()
            code = base * prime

            while code in used_values:
                if not primes:
                    raise ValueError("No hay suficientes números primos únicos disponibles.")
                prime = primes.pop()
                code = base * prime

            dictionary_of_keys[key][symbol] = code
            inverted_dict[str(code)] = symbol
            used_values.add(code)
            index += 1

        layer += 1

    return dictionary_of_keys, inverted_dict


def encode(text: List[str], dictionary_of_keys: dict) -> List[str]:
    """
    Codifica una lista de texto usando el diccionario de claves generado.

    Args:
        text (List[str]): Texto original.
        dictionary_of_keys (dict): Diccionario de codificación.

    Returns:
        List[str]: Texto codificado.
    """
    symbol_to_code = {}
    for layer in dictionary_of_keys.values():
        symbol_to_code.update(layer)

    encoded_lines = []
    for line in text:
        encoded_line = ','.join(str(symbol_to_code[char]) for char in line if char in symbol_to_code)
        encoded_lines.append(encoded_line)

    return encoded_lines


def decode(encoded_text: List[str], inverted_dict: dict) -> List[str]:
    """
    Decodifica una lista de líneas previamente codificadas.

    Args:
        encoded_text (List[str]): Texto codificado.
        inverted_dict (dict): Diccionario invertido.

    Returns:
        List[str]: Texto original decodificado.
    """
    decoded_lines = []

    for line in encoded_text:
        numbers = line.split(',')
        decoded_line = ''.join(inverted_dict.get(num.strip(), '') for num in numbers if num.strip())
        decoded_lines.append(decoded_line)

    return decoded_lines


def save_to_file(filepath: str, content: List[str]) -> None:
    """
    Guarda una lista de líneas en un archivo de texto.

    Args:
        filepath (str): Ruta del archivo.
        content (List[str]): Texto a guardar.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in content:
            f.write(line + '\n')


def load_from_file(filepath: str) -> List[str]:
    """
    Carga una lista de líneas desde un archivo de texto.

    Args:
        filepath (str): Ruta del archivo.

    Returns:
        List[str]: Texto cargado.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]


def save_dictionaries(dict1: dict, dict2: dict, base_path: str) -> None:
    """Guarda los diccionarios de codificación y decodificación en archivos JSON."""
    with open(base_path + "_encoder.json", 'w') as f:
        json.dump(dict1, f)

    with open(base_path + "_decoder.json", 'w') as f:
        json.dump(dict2, f)

def test():
    """
    Ejecuta casos de prueba para validar el sistema de codificación y decodificación.
    """
    cases = [
        ['hello my name is kopo', 'hello kopo', 'can you give a onion kopo', 'of course i will do that'],
        ['IOPOI PODI', 'DI'],
        ['12 34 19', '98 09 12 13'],
        ['////?????? ####,,,,....======'],
        ['Ho mo lo 123-123-234-55', 'Po om pol #pom', '1 + 2 = 3']
    ]

    for i, text in enumerate(cases):
        dict_keys, inv_keys = create_dictionary_of_keys(text)
        encoded = encode(text, dict_keys)
        decoded = decode(encoded, inv_keys)

        # Guardar para inspección
        save_to_file(f'test_case_{i+1}_encoded.txt', encoded)
        save_to_file(f'test_case_{i+1}_decoded.txt', decoded)
        save_dictionaries(dict_keys, inv_keys, f'test_case_{i+1}_dict')

        assert text == decoded, f'Error en el caso {i + 1}:\nEsperado: {text}\nRecibido: {decoded}'
        print(f'Caso {i + 1} exitoso')

    print("Todos los tests pasaron correctamente.")


if __name__ == '__main__':
    test()
