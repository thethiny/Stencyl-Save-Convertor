from os import write
import sys
from typing import Any, Dict, List, Union
from urllib.parse import quote, unquote
from sys import argv
import json

stencyl_literals = Union[str, int, float]
stencyl_dict = Union[Dict[str, Any]]
stencyl_list = List[stencyl_dict]
stencyl_object = Union[stencyl_dict, stencyl_list]

object_start = 'o'
array_start = 'a'
object_end = 'g'
array_end = 'h'
string = 'y'
zero = 'z'
integer = 'i'
decimal = 'd'
reference = 'R' # Duplicate Strings

strings_list: List[str] = []

save_file_name = argv[1]

with open(save_file_name, encoding='utf-8') as file:
    data: stencyl_object = json.load(file)

encoded: str = ""

def write_string(string_name: str) -> str:
    if string_name not in strings_list:
        strings_list.append(string_name)
        name = string
        string_name = quote(string_name, safe='')
        name += f"{len(string_name)}:"
        name += string_name
        return name
    else:
        return f"{reference}{strings_list.index(string_name)}"

def write_array(array: stencyl_list) -> str:
    encoded = array_start
    for element in array:
        encoded += write_object(element)
    encoded += array_end
    return encoded

def write_dict(object: stencyl_dict) -> str:
    encoded = object_start
    for key, value in object.items():
        encoded += write_string(key)
        encoded += write_object(value)
    encoded += object_end
    return encoded

def write_object(object: Union[stencyl_object, stencyl_literals]) -> str:
    encoded_data = ""

    if object == 0:
        encoded_data += zero
    elif isinstance(object, int):
        encoded_data += f"i{object}"
    elif isinstance(object, float):
        if int(object) == object:
            encoded_data += f"d{int(object)}"
        else:
            encoded_data += f"d{object}"
    elif isinstance(object, str):
        encoded_data += write_string(object)
    elif isinstance(object, dict):
        encoded_data += write_object(object)
    elif isinstance(object, list):
        encoded_data += write_array(object)

    return encoded_data


encoded = write_object(data)

with open(f"{save_file_name}.sol", 'w+', encoding='ascii') as file:
    file.write(encoded)
