"""这是“study_nester.py”模块，提供了一个名为print_lol()的
函数，用来打印列表，其中包含或不包含嵌套列表"""
def print_lol(the_list, level):
    """这个函数有一个位置参数，名为“the_list”；
       还提供了一个的缩进（制表符）数量的参数，level；
       这可以是任何Python列表（包含或不包含嵌套列表）
       所提供列表中的各个数据项会（递归地）打印到屏幕上，而且各占一行。
       你也可以使用第二个参数，指定在遇到嵌套列表前时，各个数据项之间的制表符数量"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for num_tab in range(level):
                print("\t", end='')
            print(each_item)
