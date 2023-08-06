# -*- coding:UTF-8 -*-
import sys
movies = ["Hanzhan", 2015, "shid",["list lai", 90, ["wo shi ","enen"]]]
"""以下用于多重引用"""
def print_lol(the_list):
    """处理列表中的每一项，如果是list类型，递归处理现实"""
    for each_item in the_list:
        '''ikkh'''
        if isinstance(each_item, list):
                print_lol(each_item)
        else:
            print(each_item)
if __name__ == '__main__':
    print_lol(movies)
    print(sys.path)