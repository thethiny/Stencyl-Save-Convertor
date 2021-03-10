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
real = 'R' # Possible Enumerate

rvalue = '<R>'

save_file_name = argv[1]

with open(save_file_name, encoding='utf-8') as file:
    data: Union[stencyl_object, List[stencyl_object]] = json.load(file)

if isinstance(data, dict):
    data = [data]

encoded = ""

def write_string(string_name):
    name = ""
    name += string
    string_name = quote(string_name)
    name += str(len(string_name)) + ':'
    name += string_name
    return name

def write_array(array):
    encoded = 'a'
    for element in array:
        encoded += write_string(element)
    encoded += 'h'
    return encoded

def write_object(object: stencyl_object):
    encoded_data = ""

    encoded_data += object_start

    for key, value in object.items():
        encoded_data += write_string(key)
        if value == 0:
            encoded_data += zero
        elif isinstance(value, int):
            encoded_data += f"i{value}"
        elif isinstance(value, float):
            if int(value) == value:
                encoded_data += f"d{int(value)}"
            else:
                encoded_data += f"d{value}"
        elif isinstance(value, str):
            if value.startswith(rvalue):
                # RValue
                value = float(value[len(rvalue):])
                if int(value) == value:
                    encoded_data += f"R{int(value)}"
                else:
                    encoded_data += f"R{value}"
            else:
                encoded_data += write_string(value)
        elif isinstance(value, dict):
            encoded_data += write_object(value)
        elif isinstance(value, list):
            encoded_data += write_array(value)


    encoded_data += object_end
    return encoded_data

for object in data:
    encoded += write_object(object)
    

with open(f"{save_file_name}.stencyl", 'w+', encoding='ascii') as file:
    file.write(encoded)


