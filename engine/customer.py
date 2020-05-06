#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 05 03
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

def customer_interface(conn, user):
    cursor = conn.cursor()

    bar = str("\n" + ("-" * 25) + "\n")

    command = ""
    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       (Fore.GREEN if cm else "") + "exit" + (Fore.RESET if cm else "") + ": exit the program\n" +
                       (Fore.GREEN if cm else "") + "help" + (Fore.RESET if cm else "") + ": display commands list\n" +
                       (Fore.GREEN if cm else "") + "checkout" + (Fore.RESET if cm else "") + ": purchase items\n" +
                       (Fore.GREEN if cm else "") + "inventory" + (Fore.RESET if cm else "") + ": view items available for purchase\n" +
                       "") 
    print(command_list)


    while True:

        command = get_cmd()

        if (engine.quit(command)):
            break
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

        elif command == "inventory":
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                                     "' ORDER BY sold_last_month DESC").fetchall(), cursor.description)
            continue
        #

        else:
            print("Invalid command entered.")
            print(command_list)
    
    #End while command != exit

#end customer_interface()
                    