#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 26
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sqlite3
import random
import engine
from engine import get_cmd
import order

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


###############################################################################

def associate_interface(conn, user):
    cursor = conn.cursor()

    bar = str("\n" + ("-" * 25) + "\n")

    command = ""
    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       (Fore.GREEN if cm else "") + "exit" + (Fore.RESET if cm else "") + ": exit the program\n" +
                       (Fore.GREEN if cm else "") + "help" + (Fore.RESET if cm else "") + ": display commands list\n" +
                       (Fore.GREEN if cm else "") + "checkout" + (Fore.RESET if cm else "") + ": checkout a customer\n" +
                       (Fore.GREEN if cm else "") + "order" + (Fore.RESET if cm else "") + ": view orders and order new inventory items\n" +
                       (Fore.GREEN if cm else "") + "stock" + (Fore.RESET if cm else "") + ": add received items to the inventory\n" +
                       "") 
    print(command_list)


    while(command != "exit"):

        command = get_cmd()

        if command == "exit":
            continue
        #

        elif command == "help":
            print(command_list)
            continue
        #

        elif command == "checkout":
            order.checkout(conn, user)
            print(command_list)
            continue
        #end command == checkout


        elif command == "order":
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                      "' ORDER BY stock ASC").fetchall(), cursor.description)
            order.reorder(conn, user)
            print(command_list)
            continue
        #

        elif command == "stock":
            order.restock(conn, user)
            print(command_list)
            continue
        #

        else:
            print("Invalid command entered.")
            print(command_list)
    
    #End while command != exit

#end associate_interface()
                    