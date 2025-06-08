# Description
This program is a encode system that use the structure of a Binary Tree

# Status of the Project
Version 1.0

# Oficial repository
You can find this program also in:
https://pypi.org/project/EUBTA/

# Download
## Download Library
```
pip install EUBTA
```

## Download Program
```
git clone https://github.com/White-Mask-230/Encode-Using-Binary-Tree.git
cd Encode-Using-Binary-Tree
```

Note: It haven' t use external librarys so that's all.

# Content
(All functions)
* **create_dictionary_of_keys** Arguments: _text_ -> `Tuple[str, str]`
* **encode** Arguments: _text_ -> `list[str]`; _dictionary_of_keys_ -> `str`
* **decode** Arguments: _text_ -> `list[str]`; _invert_dictionary_of_keys_ -> `List[str]`

# Example of use
``` python
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
```

# Contact
lucasvarelacorrea@gmail.com

# Make by
* [White-Mask-230 (Lucas Varela Correa)](https://github.com/White-Mask-230)
