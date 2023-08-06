#!/usr/bin/env python

import sys
from itertools import product

__version__ =  "0.1"

def full_version():
    """Returns version of current mergerpy."""
    from struct import calcsize
    return "mergerpy {} on Python {} {}-bit, {}-bit unicodes".format(
        __version__,
        ".".join(str(i) for i in sys.version_info[:3]),
        calcsize(b"P") * 8,
        sys.maxunicode.bit_length(),
    )

def load_file(filename):
    """Loads given text file from directory into string lines.
    Args:
      filename (str): Input file name.
    """
    with open(filename, 'r') as payload_file:
        lines = []
        for line in payload_file:
            lines.append(line)
        return lines

def parse_input(lines):
    """Parse given input array that contains string lines.
    Args:
      lines (array): String lines of array.
    """
    parsed_input = []
    for line in lines:
        parsed_data = line.split()
        parsed_input.append(parsed_data)
    return parsed_input

def merge_input(input_array):
    """Merges concatanates given input array into lines of strings.
    Args:
      input_array (array): Parsed string of array.
    """
    product(*input_array)
    with open('merged.txt', 'w') as merged_file:
        for input_list in product(*input_array):
            merged_str = ''.join(str(e) for e in input_list)
            merged_file.write(merged_str + '\n')
    merged_file.close()
    print('Merged file created successfully!')
    return True

def main(filename):
    """Main function which combines all three worker functions.
    Args:
      filename (str): Input file name.
    """
    lines = load_file(filename)
    parsed_input = parse_input(lines)
    return merge_input(parsed_input)
