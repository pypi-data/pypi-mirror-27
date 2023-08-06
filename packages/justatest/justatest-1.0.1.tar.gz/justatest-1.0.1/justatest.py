"""level参数用来在遇到嵌套列表时插入制表符"""
def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            
            for tab_stop in range(level):
                print ("\t",end='')
            print(each_item)
            
            
