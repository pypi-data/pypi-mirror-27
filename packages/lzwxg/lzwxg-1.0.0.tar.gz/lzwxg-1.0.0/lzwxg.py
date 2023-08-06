'''这个函数的作用是打印列表（包含N个嵌套）'''



#递归函数
def print_dg(the_list):

  for ea_it in the_list:
    if isinstance(ea_it,list):
        print_dg(ea_it)
    else:
        print(ea_it)
#结束
