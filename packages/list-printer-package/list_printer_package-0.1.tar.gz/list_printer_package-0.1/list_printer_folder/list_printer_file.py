#!/usr/bin/env python
""" A module to print the contents of nested lists
intended for testing uploading packages to Warehouse"""
__author__ = "Laura Hampton"
__credits__ = ["Sumana Harihareswara", "Laura Hampton"]
__license__ = "MIT License"
__status__ = "Prototype"


def list_printer_func(a_list):
    """prints the contents of nested lists"""
    for element in a_list:
        if not isinstance(element, list):
            print(element)
        else:
            list_printer(element)



if __name__ == '__main__':
    list_printer() 