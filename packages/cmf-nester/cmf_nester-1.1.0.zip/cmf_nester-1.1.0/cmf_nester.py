""" This module in compounded by functiona developend on the second chapter of the book head first - Phyton"""

def print_lol(the_list,level):
        """ This function searches for elements in a nested list and print them
		a second argumente is used to pusha tab whenever a nested list is found"""
        for element in the_list:
                if isinstance(element,list):
                        print_lol(element,level+1)
                else:
                        for tab_stop in range(level):
							print("t",end = '')
						print(element)
