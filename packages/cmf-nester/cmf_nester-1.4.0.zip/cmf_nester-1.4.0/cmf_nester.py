""" This module in compounded by functiona developend on the second chapter of the book head first - Phyton"""
import sys

def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
	""" This function searches for elements in a nested list and print them
		a second argumente is used to push a tab whenever a nested list is found
		in this version, a control for disabling/enablin identation is also provided
		besides that, you're also able to chage the defaut output to a specific file"""
	for element in the_list:
		if isinstance(element,list):
			print_lol(element,indent,level+1,fh)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t", end='',file=fh)
			print(element,file=fh)
					