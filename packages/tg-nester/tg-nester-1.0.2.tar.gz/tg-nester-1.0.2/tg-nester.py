#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Este módulo é somente para teste
"""

def print_list(the_list, level=0):
    for each_item in the_list:
        """
        Checa a se o item é uma lista e o level de identação
        """
        if isinstance(each_item, list):
            print_list(each_item, level + 1)
        else:
            for tab_stop in range (level):
                print("\t", end='')
            print(each_item)

movies = ['teste','teste1','teste2',['a','a1','a2',['b1','b2','b3']]]
print_list(movies, 0) 