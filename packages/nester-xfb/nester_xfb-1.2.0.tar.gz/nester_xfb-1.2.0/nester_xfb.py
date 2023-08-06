'这是一个模块，名字是nester_xfb'
'提供了一个名为print_lol()的函数'
def print_lol(the_list,level=0):
    """这是一个可递归输出列表的函数
参数是the_list"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tap_stop in range(level):
                print('\t',end='')
            print(each_item)
