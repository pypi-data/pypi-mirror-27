""" This module in compounded by functiona developend on the second chapter of the book head first - Phyton"""

def print_lol(the_list,indent=False,level=0):
	""" This function searches for elements in a nested list and print them
		a second argumente is used to push a tab whenever a nested list is found
		in this version, a control for disabling/enablin identation is also provided"""
	for element in the_list:
		if isinstance(element,list):
			print_lol(element,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t", end='')
			print(element)
					