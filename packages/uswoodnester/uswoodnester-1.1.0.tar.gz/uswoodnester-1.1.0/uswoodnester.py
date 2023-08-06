"""This is standard function to print nested list"""
def print_lol(the_list,level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)#重新递归，并用level计数嵌套数量
		else:
			for tab_stop in range(level):#碰到非列表了，根据当前计数输出制表符
				print("\t", end = '')#end表示以什么结尾，默认\n
			print(each_item)

cast = ["Palin", "Cleese", "Jones", "Gillam", "Chapman",
		["1923", "1454", "2241", "4242",
		["THe Holy","The wood","the hash"]]]

print_lol(cast, 0)
