import sys
from urllib.parse import quote, unquote
from sys import argv, is_finalizing
import enum
import json

object_start = 'o'
array_start = 'a'
object_end = 'g'
array_end = 'h'
string = 'y'
zero = 'z'
integer = 'i'
decimal = 'd'
real = 'R'

save_file_name = argv[1]

with open(save_file_name, encoding='utf-8') as file:
    data = file.read().strip()

decoded = ""
idx = 0

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
    while char in '1234567890.-':
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
is_array = False

while idx < len(data):
    char = get_char()
    if char == object_start:
        decoded += "{"
        continue
    elif char == object_end:
        decoded = remove_trailing_comma(decoded)
        decoded += "}"
        continue
    elif char == array_start:
        decoded += '['
        is_array = True
        continue
    elif char == array_end:
        decoded = remove_trailing_comma(decoded)
        decoded += ']'
        is_array = False
        continue
    elif char == string:
        length = get_length()
        name = read_name(length)
        decoded += f'"{name}"'
    elif char == integer:
        value = get_integer()
        decoded += str(value)
    elif char == real or char == decimal:
        value = get_float()
        decoded += str(value)
    elif char == zero:
        decoded += '0'
    else:
        raise Exception(f"Unknown Character {char}")
    
    if is_key and not is_array:
        decoded += ": "
    else:
        decoded += ','
    
    is_key = not is_key



with open(f"{save_file_name}.json", 'w+', encoding='utf-8') as file:
    file.write(decoded)


