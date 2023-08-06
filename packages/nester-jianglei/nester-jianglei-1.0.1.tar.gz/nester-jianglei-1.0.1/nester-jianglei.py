#!/usr/bin/env python
# coding: utf8

"""这是 "wester.py"模块，提供了一个名为print_lol()的函数，这个函数
的作用是打印列表，其中有可能包含(也可能不包含)嵌套列表。"""

def print_lol(the_list,tab=False, level=-1):
    """这个函数取一个位置参数，名为"the_list"，这可以是任何python
    列表(也可以是包含嵌套列表的列表)。所指定的列表中的每个数据项会
    (递归地)输出到屏幕上，各数据项各占一行。"""
    if isinstance(the_list, list):
        for item in the_list:
            print_lol(item, tab=tab, level=level + 1)
    else:
        if tab:
            print('\t' * level, end='')
        print(the_list)

if __name__ == "__main__":
    lit = ['a', ['a', 'b',['c']]]
    print_lol(lit, tab=True)
