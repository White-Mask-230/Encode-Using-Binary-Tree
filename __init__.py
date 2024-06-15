import random

def create_dictionary_of_keys(symbols=None):
    """ unsupported numbers """

    max_number = random.randint(150, 300)
    prime_numbers = []

    if not symbols:
        symbols = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']

    for i in range(2, max_number):
        z = 0
            
        for j in range(2, i):
            if i % j == 0:
                z = 1
                break

        if z == 0:
            prime_numbers.append(i)
        
    dictionary_of_keys = {"layer 0" : {symbols[0] : random.choice(prime_numbers)}, "layer 1" : {}}
        
    del symbols[0]
    
    layer = 1
    id_previous_layer = 0 # Its function is to select the upstream element that must be added two other elements
    counter = 0 # Its function is to ensure that only two elements are assigned to the upstream element.
    i = 1 # Its function is to ensure that an empty layer is not created

    for symbol in symbols:        
        random_number = random.choice(prime_numbers)
        value_1_upstream = list(dictionary_of_keys[f'layer {id_previous_layer}'].values())[id_previous_layer] 

        dictionary_of_keys[f'layer {layer}'][symbol] = value_1_upstream * random_number

        if len(list(dictionary_of_keys[f'layer {layer}'].values())) == 2 ** layer:
            # a new layer is created
            
            if len(symbols) == i: # prevents an empty layer from being created
                break

            layer += 1
            id_previous_layer = 0
            dictionary_of_keys[f'layer {layer}'] = {}
        else: 
            # checks if the upstream element needs to be changed
            
            if counter == 2:
                id_previous_layer += 1
                counter = 0

            else:
                counter += 1

        i += 1
    
    #BUG Two letters can have the same value, which means that when one is deciphered, it appears as many times as the other should appear.

    return dictionary_of_keys

def encode(text: list[str], dictionary_of_keys):
    encode_text = []
    
    for line in text:
        for i in range(len(dictionary_of_keys)):
            layer = dictionary_of_keys[f"layer {i}"]
                
            for j in range(len(layer)):
                symbol = list(layer.keys())[j]
                encode_symbol = str(list(layer.values())[j]) + ','

                line = line.replace(symbol, encode_symbol)

        encode_text.append(line)

    return encode_text

def decode(text: list[str], dictionary_of_keys):
    # reverse the dictionary
    inverted_dict = {}
    for layer, chars in dictionary_of_keys.items():
        for char, num in chars.items():
            inverted_dict[str(num)] = char

    decode_text = []

    for line in text:
        decode_line = []

        for word in line.split(', '):
            decode_word = []

            for number in word.split(','):
                decode_letter = inverted_dict.get(str(number.strip()), '')
                decode_word.append(decode_letter)
            
            decode_word_join = ''.join(decode_word)
            decode_line.append(decode_word_join)

        decode_line_join = ' '.join(decode_line)
        decode_text.append(decode_line_join)

    return decode_text

def test():
    text = ['hello my name is kopo', 'hello kopo', 'can you give a onion kopo', 'of course I will do that']

    dictionary_of_keys = create_dictionary_of_keys()

    encode_text = encode(
        text=text,
        dictionary_of_keys=dictionary_of_keys
    )

    decode_text = decode(
        text=encode_text,
        dictionary_of_keys=dictionary_of_keys
    )

    if text == decode_text:
        return True
    else:
        return False

if __name__ == '__main__':
    #print(test())

    dictionary_of_keys = create_dictionary_of_keys()

    encode_text = encode(
        text=['hello my name is kopo', 'hello kopo', 'can you give a onion kopo', 'of course I will do that'],
        dictionary_of_keys=dictionary_of_keys
    )

    print(encode_text)

    decode_text = decode(
        text=encode_text,
        dictionary_of_keys=dictionary_of_keys
    )

    print(dictionary_of_keys)
    print(decode_text)