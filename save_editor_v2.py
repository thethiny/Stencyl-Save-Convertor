from os import read
import sys
from urllib.parse import quote, unquote
from sys import argv, is_finalizing
import enum
import json

object_start = 'o'
array_start = 'a'
set_start = 'b' # Tuple or Set
object_end = 'g'
array_end = 'h'
set_end = 'h'
string = 'y'
zero = 'z'
integer = 'i'
decimal = 'd'
reference = 'R' # String Counter, counts number of strings to use them as Reference

rvalue = '<R>'

save_file_name = argv[1]

with open(save_file_name, encoding='utf-8') as file:
    data = file.read().strip()

decoded = ""
idx = 0
strings_list = []

def adjust_index(val=1):
    global idx
    idx += val

def get_char():
    char = data[idx]
    adjust_index()
    return char

def get_length():
    char = get_char()
    digits = ""
    while char != ':':
        digits += char
        char = get_char()
    return int(digits)

def get_integer():
    char = get_char()
    digits = ""
    while char in '1234567890-':
        digits += char
        char = get_char()
    adjust_index(-1)
    return int(digits)

def get_float():
    char = get_char()
    digits = ""
    while char in '1234567890.-+e':
        digits += char
        char = get_char()
    adjust_index(-1)
    return float(digits)

def read_name(length):
    name = ""
    for i in range(length):
        name += get_char()
    return unquote(name)

def remove_trailing_comma(string):
    if string[-1] == ',':
        return string[:-1]
    return string

is_key = True

def read_string():
    length = get_length()
    name = read_name(length)
    strings_list.append(name)
    return f'"{name}"'

def read_integer():
    value = get_integer()
    return str(value)

def read_real():
    value = get_integer()
    return f'"{strings_list[value]}"'
    # return f"\"{rvalue}{value}\""

def read_float():
    value = get_float()
    return str(value)

def read_object(decoded, is_key, is_array=False):
    char = get_char()
    if char == object_start:
        decoded += "{"
        while data[idx] != object_end:
            decoded, is_key = read_object(decoded, is_key)
        return decoded, is_key
    elif char == object_end:
        decoded = remove_trailing_comma(decoded)
        decoded += "},"
        return decoded, is_key
    elif char == array_start or char == set_start:
        decoded += '['
        while data[idx] != array_end:
            decoded, is_key = read_object(decoded, is_key, True)
        return decoded, is_key
    elif char == array_end:
        decoded = remove_trailing_comma(decoded)
        decoded += '],'
        return decoded, is_key
    elif char == string:
        decoded += read_string()
    elif char == integer:
        decoded += read_integer()
    elif char == reference:
        decoded += read_real()
    elif char == decimal:
        decoded += read_float()
    elif char == zero:
        decoded += '0'
    else:
        raise Exception(f"Unknown Character {char} at index {idx}")

    if is_key and not is_array:
        decoded += ": "
    else:
        decoded += ','
    
    is_key = not is_key
    
    return decoded, is_key

# while idx < len(data):
if data[0] == object_start:
    decoded, is_key = read_object(decoded, is_key)
    decoded = remove_trailing_comma(decoded)
    decoded += '}'
elif data[0] in [array_start, set_start]:
    decoded, is_key = read_object(decoded, is_key, True)
    decoded = remove_trailing_comma(decoded)
    decoded += ']'


with open(f"{save_file_name}.json", 'w+', encoding='utf-8') as file:
    file.write(decoded)


