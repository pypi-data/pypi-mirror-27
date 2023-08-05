"""
这是nest.py模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表，
其中有可能包含(也可能不包含)嵌套列表

"""
#递归
def print_lol(the_list):
    """
    位置参数the_list 这可以是任何Python 列表，也可以是包含嵌套列表的列表。所指定的列表中的每一个数据项
    会递归输出到屏幕上，各数据项各占一行
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item);
        else:
            print(each_item);
