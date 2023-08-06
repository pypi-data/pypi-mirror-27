'这是一个模块，名字是nester_xfb'
'提供了一个名为print_lol()的函数'
def print_lol(the_list, indent=False, level=0):
    """这是一个可递归输出列表的函数
参数是the_list"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tap_stop in range(level):
                     print('\t',end='')
            print(each_item)
