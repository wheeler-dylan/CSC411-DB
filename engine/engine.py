#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import os

def clear_screen():
    try:
        clear = lambda: os.system("cls") #on Windows System
        clear()
    except:
        clear = lambda: os.system("clear") #on Linux System
        clear()
#


def set_length(f_string = "", f_length = 16):
    return str("{:<16}".format(str(f_string))[:f_length])

def print_cursor_fetch(f_fetch, f_headers = None):
    if f_headers != None:
        for each_attribute in [i[0] for i in f_headers]:
            print(set_length(each_attribute), end=" ")
        print()
    for each_tuple in f_fetch:
        for each_cell in each_tuple:
            print(set_length(each_cell), end=" ")
        print()