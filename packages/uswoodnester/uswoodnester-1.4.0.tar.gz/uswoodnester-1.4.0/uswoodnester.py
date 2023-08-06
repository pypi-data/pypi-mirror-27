"""This is standard function to print nested list"""
def print_lol(the_list, indent=False, level=0, fn=sys.stdout):#设置一个布尔控制是否缩进，设置一个可选参数控制缩进次数，默认为0,fn控制输出的到文件
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item, indent, level+1, fn)#重新递归，并用level计数嵌套数量,这里需要重新调用indent
		else:
			if indent:
				for tab_stop in range(level):#碰到非列表了，根据当前计数输出制表符
					print("\t", end = '', file =fn)#end表示以什么结尾，默认\n，这里用''表示关闭换行
			print(each_item, file=fn)

cast = ["Palin", "Cleese", "Jones", "Gillam", "Chapman",
		["1923", "1454", "2241", "4242",
		["THe Holy","The wood","the hash"]]]

print_lol(cast,True, 2)
