"""这是“study_nester.py”模块，提供了一个名为print_lol()的
函数，用来打印列表，其中包含或不包含嵌套列表"""
def print_lol(the_list, indent=False, level=0):
    """这个函数有三个参数，其中第一个参数为必选参数，名为“the_list”；
       第二个参数是可选参数，用户可以使用该参数决定是否打印制表符，默认不打印；
       第三个是可选一个的缩进（制表符）数量的参数，level；
       这可以是任何Python列表（包含或不包含嵌套列表）
       所提供列表中的各个数据项会（递归地）打印到屏幕上，而且各占一行。"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for num_tab in range(level):
                    print("\t", end='')
            print(each_item)
