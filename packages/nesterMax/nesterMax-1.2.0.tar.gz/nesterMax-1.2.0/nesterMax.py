"""這是 "nester.py" 模塊, 提供了一個名為print_lol的函數,這個函數的作用是打印列表,其中有可能包含(也可能不包含)嵌套列表."""
def print_lol(the_list,level=0):
	"""這個函數取一個位置參數,名為 "the_list" , 這可以是任何python列表(也可以是包含嵌套的列表). 
	所指定的列表中的每個數據項目會(遞迴地)輸出到屏幕上,個數據各占一行."""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
			    print("\t", end='')
			print(each_item)
