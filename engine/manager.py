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

    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id = '" + str(user.store_id) + "';").fetchall(), cursor.description)
    print()

    bar = str("\n" + ("-" * 25) + "\n")

    command = ""
    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       (Fore.GREEN if cm else "") + "exit" + (Fore.RESET if cm else "") + ": exit the program\n" +
                       (Fore.GREEN if cm else "") + "help" + (Fore.RESET if cm else "") + ": display commands list\n" +
                       #(Fore.GREEN if cm else "") + "orders" + (Fore.RESET if cm else "") + ": view all orders made\n" +
                       (Fore.GREEN if cm else "") + "bestsellers" + (Fore.RESET if cm else "") + ": view best selling items at your location\n" +
                       (Fore.GREEN if cm else "") + "employ" + (Fore.RESET if cm else "") + ": hire or fire an associate\n" +
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
            order_mode(conn, user)
            print(bar)
            continue
        #

        else:
            print("Invalid command entered.")
            print(command_list)
    
    #End while command != exit

#end manager_interface()




def order_mode(conn, user):
    
    cursor = conn.cursor()
    command = ""

    while not engine.quit(command, "Exiting order mode."):

        command = get_cmd("\nSelect from the following commands:\n" +
                          (Fore.GREEN if cm else "") + "orders" + (Fore.RESET if cm else "") + ": view recent orders\n" +
                          (Fore.GREEN if cm else "") + "details" + (Fore.RESET if cm else "") + ": view a detailed order report\n" +
                          (Fore.GREEN if cm else "") + "inventory" + (Fore.RESET if cm else "") + ": view current inventory by lowest stock\n" +
                          (Fore.GREEN if cm else "") + "reorder" + (Fore.RESET if cm else "") + ": order more items\n" +
                          (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + " exit order mode\n" +
                          "")

        if engine.quit(command, "Exiting order mode."):
            return

        elif command == "orders":
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM orders WHERE store_id='" + str(user.store_id) +
                                                     "' ORDER BY date DESC").fetchall(), cursor.description)
            continue

        elif command == "details":
            input = get_cmd("Enter the " + (Fore.CYAN if cm else "") + 
                            "Order ID" + (Fore.RESET if cm else "") + 
                            " of the order you'd like to view.") 

            if (engine.quit(input, "Exiting order mode.")):
                return


            while int(input) not in [i[0] for i in cursor.execute("SELECT id FROM orders WHERE " +
                                                                  "id = '" + str(input) + "';").fetchall()]: 
                input = get_cmd("Order ID not found, please re-enter Order ID, or type "+ 
                                (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + 
                                " to cancel.") 

                if (engine.quit(input), "Exiting order mode."):
                    return

            #end while id not found

            #once id is found
            order_id = int(input)

            #get itemization id
            try:
                itemization_id = str(engine.get_cell(conn, "itemization_id", "orders", "id", str(order_id)))
                print("Loading itemized order list: " + itemization_id + "...")
            except sqlite3.Error as error:
                print((Fore.RED if cm else "") + 
                      "Error collecting Itemization ID from order table:" +
                      (Fore.RESET if cm else ""))
                print(error)
                print("Exiting order mode.")
                return

            else:
                print("Displaying itemization details for Order " + str(order_id) + ":")
                engine.print_cursor_fetch(cursor.execute("SELECT * FROM " + str(itemization_id)), cursor.description)



        #end command = details


        elif command == "inventory":
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                                     "' ORDER BY stock ASC").fetchall(), cursor.description)
            continue

        elif command == "reorder":

            #get inventory id for items to order
            input = get_cmd("Enter the " + 
                            (Fore.CYAN if cm else "") + "Inventory ID" + (Fore.RESET if cm else "") + 
                            " of the item you'd like to restock.")

            if (engine.quit(input, "Exiting order mode.")):
                return


            while int(input) not in [i[0] for i in cursor.execute("SELECT id FROM inventory WHERE " +
                                                             "id = '" + input + "';").fetchall()]: 
                input = get_cmd("Inventory ID not found, please re-enter Inventory ID, or type "+ 
                                (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + 
                                " to cancel.") 

                if (engine.quit(input), "Exiting order mode."):
                    return

            #end while id not found

            #once id is found
            reorder_id = int(input)

            #get quantity
            while True:
                try:
                    input = get_cmd("Enter the " + 
                                    (Fore.CYAN if cm else "") + "quantity" + (Fore.RESET if cm else "") + 
                                    " of the item you'd like to restock.")

                    if (engine.quit(input, "Exiting order mode.")):
                        return
                    #

                    input = int(input)

                except ValueError as error:
                    print("Error, please enter an integer.")
                    continue

                else:
                    reorder_quantity = int(input)
                    break 
            


            #TODO: implement itamization and format order

            print("Ordering " + str(reorder_quantity) + " of item " + str(reorder_id) + "...")

            continue
        #end command = reorder

        else:
            print("Error, invalid command entered.")
            continue

    #End while

#End order_mode()



        