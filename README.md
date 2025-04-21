# Description
This program is a encode system that use the structure of a Binary Tree

# Status of the Project
Beta 5.0

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

# Simple example of use
## Content
(All functions)
* **create_dictionary_of_keys** Arguments: _text_ -> `list[str]`
* **encode** Arguments: _text_ -> `list[str]`; _dictionary_of_keys_ -> `dict[str][int]`
* **decode** Arguments: _text_ -> `list[str]`; _invert_dictionary_of_keys_ -> `dict[str][int]`

## Example of use
``` python
import EUBTA

text = ['hi all', 'no hi all', 'lion in a dragon', 'every one dancing right now']

dictionary_of_keys, invert_dictionary_of_keys = create_dictionary_of_keys(text)
encode_text = encode(
    text=text,
    dictionary_of_keys=dictionary_of_keys
)
decode_text = decode(
    text=encode_text,
    invert_dictionary_of_keys=invert_dictionary_of_keys
)

print(f'Dictionary of keys: {dictionary_of_keys}')
print(f'Encode text: {encode_text}')
print(f'Decode text: {decode_text}')
```

# Contact
lucasvarelacorrea@gmail.com

# Make by
* [White-Mask-230 (Lucas Varela Correa)](https://github.com/White-Mask-230)
