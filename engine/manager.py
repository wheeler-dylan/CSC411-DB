#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 26
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sqlite3
import random
import engine
from engine import get_cmd

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

def manager_interface(conn, user):
    cursor = conn.cursor()

    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id = '" + user.store_id + "';").fetchall(), cursor.description)
    print()

    bar = str("\n" + ("-" * 25) + "\n")

    command = ""
    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       (Fore.GREEN if cm else "") + "exit" + (Fore.RESET if cm else "") + ": exit the program\n" +
                       (Fore.GREEN if cm else "") + "help" + (Fore.RESET if cm else "") + ": display commands list\n" +
                       (Fore.GREEN if cm else "") + "orders" + (Fore.RESET if cm else "") + ": view all orders made and amounts sold\n" +
                       (Fore.GREEN if cm else "") + "bestsellers" + (Fore.RESET if cm else "") + ": view best selling items at your location\n" +
                       (Fore.GREEN if cm else "") + "employ" + (Fore.RESET if cm else "") + ": hire or fire an associate\n" +
                       (Fore.GREEN if cm else "") + "order" + (Fore.RESET if cm else "") + ": order new inventory items\n" +
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

        elif command == "orders":
            continue
        #

        elif command == "bestsellers":
            print(bar)

            engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                                     "' ORDER BY sold_last_month DESC LIMIT 3").fetchall(), cursor.description)

            print(bar)
            continue
        #

        elif command == "order":
            print(bar)
            rorder_mode()
            print(bar)
            continue
        #
    
    #End while command != exit

#end manager_interface()




def order_mode():
    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                                "' ORDER BY stock DESC").fetchall(), cursor.description)

    input = get_cmd("Would you like to reorder items? Enter " + 
                    (Fore.GREEN if cm else "") + "YES" + (Fore.RESET if cm else "") + 
                    ", all other input will cancel.")

    if input != "YES":
        print("Exiting restock mode.\n")
        return

    #get inventory id for items to order
    input = get_cmd("Enter the " + 
                    (Fore.CYAN if cm else "") + "Inventory ID" + (Fore.RESET if cm else "") + 
                    " of the item you'd like to restock.")

    while input not in [i[0] for i in cursor.execute("SELECT id FROM inventory WHERE " +
                                                     "id = '" + input + "';").fetchall()]: 
        input = get_cmd("Inventory ID not found, please re-enter Inventory ID, or type "+ 
                        (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + 
                        " to cancel.") 

        if (engine.quit(input), "Exiting restock mode."):
            return

    #end while id not found

    #once id is found
    restock_id = input

    #get quantity
    input = get_cmd("Enter the " + 
                    (Fore.CYAN if cm else "") + "quantity" + (Fore.RESET if cm else "") + 
                    " of the item you'd like to restock.")



#



        