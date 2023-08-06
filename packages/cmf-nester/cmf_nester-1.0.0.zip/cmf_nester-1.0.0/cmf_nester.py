""" This module in compounded by functiona developend on the second chapter of the book head first - Phyton"""

def print_lol(the_list):
        """ This function searches for elements in a nested list and print them"""
        for element in the_list:
                if isinstance(element,list):
                        print_lol(element)
                else:
                        print(element)
