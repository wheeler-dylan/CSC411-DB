#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import os

#use formatted text colors if library is available
try:
    import colorama
except Exception as error:
    print(error)
    cm = False
else:
    colorama.init()
    from colorama import Fore, Back, Style
    cm = True
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
    print((Fore.YELLOW if cm else ""))
    cmd = input()
    print((Fore.RESET if cm else ""), end="")
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
            print((Fore.CYAN if cm else "") + set_length(each_attribute) + (Fore.RESET if cm else ""), end=" ")
        print()
    for each_tuple in f_fetch:
        for each_cell in each_tuple:
            print(set_length(each_cell), end=" ")
        print()
#



def get_cell(f_conn, f_attribute, f_table, f_condition, f_query):
    """searches the db for a single cell value from a table,
        must be formatted outside the function call with str(), int(), etc"""
    cursor = f_conn.cursor()
    return (cursor.execute("SELECT " + f_attribute + " FROM " +
                           f_table + " WHERE " + f_condition + 
                           " ='" + f_query + "';").fetchall()[0][0])
#



def quit(f_input, f_message = ""):
    """checks input string for terms that indicate canceling
        a process and returns True if input matches one of those terms"""
    if f_input in ["cancel", "exit"]:
        print(f_message)
        return True
#