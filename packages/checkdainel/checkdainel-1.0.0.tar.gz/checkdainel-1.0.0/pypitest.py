"""这是"nester.py"模块，提供了一个名为print_lol的函数，这个函数的作用是打印列表，其中有可能包含（也有可能不包含）被嵌套列表."""

def print_lol(the_list):
    """the_list, 函数的位置参数，可以是python的任何列表，也可以是包含嵌套列表的列表。所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

"""test case"""
"""
movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,["Graham Chapman", ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
print_lol(movies)
"""