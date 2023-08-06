'''打印电影列表的每一个数据项'''
def print_list(list_m, indent=False, level=0):
	for each_item in list_m:
		if isinstance(each_item, list):
			print_list(each_item, indent, level + 1)
		else:
			if indent:
				for i in range(level):
					print('\t', end='')
			print(each_item)
