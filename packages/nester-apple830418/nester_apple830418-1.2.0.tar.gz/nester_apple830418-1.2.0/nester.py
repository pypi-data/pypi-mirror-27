# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:44:36 2017

@author: root
"""


def print_lol(the_list,leavel=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,leavel+1)
        else:
            for tab_stop in range(leavel):
                print("\t",end='')
            print(each_item)

movies = ["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
          ["Graham Chapman",
           ["Michael Palin","John Cleese", "Terry Gilliam","Eric Idle","Terry Jones"]]]
print_lol(movies,0)



