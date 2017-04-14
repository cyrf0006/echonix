#!/usr/bin/env python3

import sys
from echonix import raw
import xml.etree.ElementTree as ET

# rawcat [FILE]
# Concatenate raw files and print on the standard output

# TODO: Clean up and consistency

# TODO: Find a nicer textualisation format that could be compiled back
# into a RAW file


def print_indented_String(str, indent):
    """Prints str idented indent times"""
    print('{0}{1}'.format('   '*indent, str))


def print_node(node, indent=0):
    print_indented_String(node.tag + ":", indent)

    for a in node.attrib:
        print_indented_String('{0}: {1}'.format(a, node.get(a)), indent+1)

    for child in node:
        print_node(child, indent+1)


def print_xml(x, indent=0):
    tree = ET.fromstring(x)
    print_node(tree, indent)


def print_named_tuple(x, indent=0):
    dict = x._asdict()
    for field in x._fields:
        value = dict[field]

        if field == "xml":
            print_xml(value)
        elif field == 'datetime':
            dt = raw.python_datetime(value)
            print_indented_String('datetime: {0}'.format(dt), indent)
        elif type(value).__name__ == 'tuple':
            # unnamed tuple
            print_indented_String('{0}: {1}'.format(field, value), indent)
        elif isinstance(value, tuple):
            # named tuple
            print_indented_String(field + ':', indent)
            print_named_tuple(value, indent+1)
        else:
            print_indented_String('{0}: {1}'.format(field, value), indent)


def cat_datagram(datagram):
    print_named_tuple(datagram)


def cat_datagrams(filename):
    with open(filename, "rb") as f:
        while True:
            datagram = raw.read_encapsulated_datagram(f, raw.read_datagram)
            if not datagram:
                break

            cat_datagram(datagram)


def main():
    for filename in sys.argv[1:]:
        cat_datagrams(filename)


if __name__ == "__main__":
    main()
