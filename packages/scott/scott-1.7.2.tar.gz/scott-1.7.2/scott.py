#-*- coding:UTF-8 -*-

def print_lol(the_list,indent=False,level=0):#增加indent参数控制是否开启缩进

	for each_item in the_list:
		if isinstance(each_item,list):       #判断列表元素是否为列表
			print_lol(each_item,indent,level+1)      #若元素为列表则调用函数本身继续调用
	
		else:

			if indent:

				for tab_stop in range(level):    #根据多少层嵌套，打印多少tab
					print('\t',end='')
			
			print(each_item)

