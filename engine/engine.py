#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import os

#use formatted text colors if library is available
try:
    import colorama
    import termcolor
    """example:
    print('\033[31m' + 'some red text')
    print('\033[39m') # and reset to default color
    """
except Exception as error:
    print(error)
    color_mode = False
else:
    colorama.init()
    from colorama import Fore, Back, Style
    color_mode = True
#



def clear_screen():
    """clears the console screen, uses try to detect os"""
    try:
        clear = lambda: os.system("cls") #on Windows System
        clear()
    except:
        clear = lambda: os.system("clear") #on Linux System
        clear()
#



def get_cmd(f_prompt = ""):
    """gets a command from user and returns it
        automatically formats the text color 
        to avoid duplicate code elsewhere"""
    print(f_prompt)
    print((Fore.YELLOW if color_mode else ""))
    cmd = input()
    print((Fore.RESET if color_mode else ""), end="")
    return cmd
#



def set_length(f_string = "", f_length = 16):
    """sets the length of a given string to a specific amount
        fills the rest with spaces"""
    return str("{:<16}".format(str(f_string))[:f_length])
#



def print_cursor_fetch(f_fetch, f_headers = None):
    """function designed to output cursor.fetchall()
        calls in a formatted way for readability""" 
    if f_headers != None:
        for each_attribute in [i[0] for i in f_headers]:
            print((Fore.CYAN if color_mode else "") + set_length(each_attribute) + (Fore.RESET if color_mode else ""), end=" ")
        print()
    for each_tuple in f_fetch:
        for each_cell in each_tuple:
            print(set_length(each_cell), end=" ")
        print()
#



#def check_unique(f_conn, f_table, f_attribute = "id"):
    """searches the db for a value value from a table"""
