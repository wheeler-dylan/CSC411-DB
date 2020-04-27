#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import os
import sqlite3 

import sys
sys.path.append("./schemas")
sys.path.append("./class_definitions")
import schemas

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



def debugging_mode(connection, database_filename):
    #delete database for recreation when in debugging mode
    connection.close()
    os.remove(database_filename)
    connection = sqlite3.connect(database_filename) 
    cursor = connection.cursor() 
    #

    #build tables
    tables_list = schemas.import_schemas("schemas")
    print()
    for each_table in tables_list.values():
        try:
            each_table.print_me()
            
            print((Fore.CYAN if cm else "") +
                  str(each_table.get_query()) +
                  (Fore.RESET if cm else ""))

            cursor.execute(each_table.get_query())
        except sqlite3.Error as error:
            print((Fore.RED if cm else "") + 
                  "Error building tables from schemas folder:" +
                  (Fore.RESET if cm else ""))
            print(error)
            input("Press ENTER to continue...\n")

        print("\n")
    #

    #import data
    for each_table in tables_list.values():
        filename = str(".\\data\\" + each_table.name + ".csv")
        this_file = open(filename, 'r')
        print((Fore.MAGENTA if cm else "") + str(each_table.name) + (Fore.RESET if cm else ""))
        for each_line in this_file:
            cells = each_line.rstrip('\n').split(";")
            print(cells) #debugging
        
            try:
                print((Fore.CYAN if cm else "") + 
                      each_table.get_tuple_query(cells) + 
                      (Fore.RESET if cm else ""))
                cursor.execute(each_table.get_tuple_query(cells))
            except sqlite3.Error as error:
                print((Fore.RED if cm else "") + 
                      "Error importing tuples from data file " + filename + ":" + 
                      (Fore.RESET if cm else ""))
                print("tuple data: " + str(each_line)) 
                print(error)
                input("Press ENTER to continue...\n")
        #
        print("")
    #
    connection.commit()
# end debugging_mode()




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
    if f_input in ["cancel", "exit", "close"]:
        print(f_message)
        return True
    else:
        return False
#