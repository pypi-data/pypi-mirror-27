'''this is the standard way to include a function named print_lot'''
def print_lot(the_list):
#this function is to visit everyelement of array

	for i in the_list:
		if isinstance(i,list):#check the i
			print_lot(i)
		else:
			print(i)
