#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import PyYAML import load
config = load('teste')

"""
Este módulo é somente para teste
"""

def print_list(the_list, indent=False, level=0):
    for each_item in the_list:
        """
        Checa a se o item é uma lista e o level de identação
        """
        if isinstance(each_item, list):
            print_list(each_item, indent, level + 1)
        else:
            if indent == True :
                for tab_stop in range (level):
                    print("\t", end='')
            print(each_item) 