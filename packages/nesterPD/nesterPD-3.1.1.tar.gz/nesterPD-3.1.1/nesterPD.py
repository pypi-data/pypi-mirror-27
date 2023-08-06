"""
This is the module to include a function which prints the list items

"""

def printlist(in_list):
	"""
		printlist function iterates over each item in the list 
		and prints it
	"""
	for each_item in in_list:
		if isinstance(each_item,list):
			printlist(each_item)
		else:
			print(each_item)