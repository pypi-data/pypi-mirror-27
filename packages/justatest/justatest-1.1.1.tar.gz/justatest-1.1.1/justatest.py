"""ident参数用来指示是否需要tab缩进，level参数用来在遇到嵌套列表时插入制表符"""
def print_lol(the_list,ident=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,ident,level+1)
        else:
            if ident:
                for tab_stop in range(level):
                  print ("\t",end='')
                print(each_item)
            else:
                print(each_item)
                
            
            
