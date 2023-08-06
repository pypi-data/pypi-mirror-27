'''打印电影列表的每一个数据项'''
def print_list(list_movies):
	for each_item in list_movies:
		if isinstance(each_item, list):
			print_list(each_item)
		else:
			print(each_item)

