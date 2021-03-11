from os import write
import sys
from typing import Any, Dict, List, Union
from urllib.parse import quote, unquote
from sys import argv
import json

stencyl_object = Dict[str, Union[str, int, float, Dict[str, Any], List[str]]]

object_start = 'o'
array_start = 'a'
object_end = 'g'
array_end = 'h'
string = 'y'
zero = 'z'
integer = 'i'
decimal = 'd'
reference = 'R' # Duplicate Strings

strings_list = []

save_file_name = argv[1]

with open(save_file_name, encoding='utf-8') as file:
    data: Union[stencyl_object, List[stencyl_object]] = json.load(file)

encoded = ""

def write_string(string_name):
    if string_name not in strings_list:
        strings_list.append(string_name)
        name = string
        string_name = quote(string_name, safe='')
        name += f"{len(string_name)}:"
        name += string_name
        return name
    else:
        return f"{reference}{strings_list.index(string_name)}"

def write_array(array):
    encoded = array_start
    for element in array:
        encoded += write_object(element)
    encoded += array_end
    return encoded

def write_object(object):
    encoded_data = ""

    if isinstance(object, dict):
        encoded_data += object_start
        for key, value in object.items():
            encoded_data += write_string(key)
            encoded_data += write_object(value)
        encoded_data += object_end
    elif object == 0:
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


