"""
This is the module to include a function which prints the list items

"""

def printlist(in_list,level):
	"""
		printlist function iterates over each item in the list 
		and prints it
	"""
	for each_item in in_list:
		if isinstance(each_item,list):
			printlist(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)
