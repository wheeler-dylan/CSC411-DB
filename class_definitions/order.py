#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 05 20
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sqlite3
import random
import glob
import engine
from engine import get_cmd
from datetime import date

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

def reorder(conn, user):

    cursor = conn.cursor()

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
    #end get quantity

    #output suppliers for user reference
    print("Available Suppliers:")
    engine.print_cursor_fetch(cursor.execute("SELECT * FROM supplier;").fetchall(), cursor.description)
    print()

    #get supplier id for items to order
    input = get_cmd("Enter the " + 
                    (Fore.CYAN if cm else "") + "Supplier ID" + (Fore.RESET if cm else "") + 
                    " you would like to order from.")

    if (engine.quit(input, "Exiting order mode.")):
        return


    while int(input) not in [i[0] for i in cursor.execute("SELECT id FROM supplier WHERE " +
                                                        "id = '" + input + "';").fetchall()]: 
        input = get_cmd("Supplier ID not found, please re-enter Supplier ID, or type "+ 
                        (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + 
                        " to cancel.") 

        if (engine.quit(input), "Exiting order mode."):
            return

    #end while supplier id not found

    supplier_id = int(input)



    #generate itemization id

    #find id that is unique
    untrimmed_itemization_list = glob.glob(str(".\\itemization\\*.csv"))
    itemization_list = []
    for each_item in untrimmed_itemization_list:
        itemization_list.append(str(each_item.replace(".\\itemization\\", "").replace(".csv", "")))
    while True:
        item_id = random.randint(11111111, 99999999)
        item_id = str("i" + str(item_id))
        if item_id in itemization_list:
            continue #if exists, try again
        else:
            break #if unique, move on
    #

    #create itemization table
    try:
        query = str(engine.get_itemization_query(item_id))
        cursor.execute(query)

    except sqlite3.Error as error:
        print((Fore.RED if cm else "") + 
               "Error building itemization table for " + str(item_id) + ":" +
               (Fore.RESET if cm else ""))
        print(query)
        print(error)

    else:
        try:
            this_row_id = str(random.randint(11111111, 99999999))   #get random id for item row
            this_row_category = str(engine.get_cell(conn, "category", "inventory", "id", reorder_id))   #get category from inventory table
            this_row_item_id = str(engine.get_cell(conn, "item_id", "inventory", "id", reorder_id))     #get item_id from inventory table
            this_row_price = str(engine.get_cell(conn, "price", this_row_category, "id", this_row_item_id))       #get quantity to be ordered

            query = str("INSERT INTO " + item_id + " VALUES ('401" +
                        str(this_row_id) + "', '" +    
                        str(this_row_category) + "', '" +  
                        str(this_row_item_id) + "', '" +  
                        str(reorder_quantity) + "', '" +      
                        str(this_row_price) +
                        "');")
                    
            cursor.execute(query)

        except sqlite3.Error as error:
            print((Fore.RED if cm else "") + 
                  "Error populating itemization table for " + str(item_id) + ":" +
                  (Fore.RESET if cm else ""))
            print(query)
            print(error)

        else:
            #add order to orders table
            try:
                #get unique order id
                while True:
                    this_order_id = random.randint(11111111, 99999999)
                    if this_order_id in [i[0] for i in cursor.execute("SELECT id FROM orders;")]:
                        continue #if exists, try again
                    else:
                        break #if unique, move on
                #
                
                grand_total = float(float(reorder_quantity) * float(this_row_price))

                query = str("INSERT INTO orders VALUES ('" +
                            str(this_order_id) + "', '" +    
                            str(date.today()) + "', '" +  
                            str(user.store_id) + "', '" + 
                            str(supplier_id) + "', '" +
                            str(user.id) + "', '" +      
                            str(item_id) + "', '" +
                            str(grand_total) +
                            "');")

                print("Ordering " + str(reorder_quantity) + " of item " + 
                      str(engine.get_cell(conn, "name", "inventory", "id", reorder_id)) +
                      "...")
                print(query)
                    
                cursor.execute(query)
            except sqlite3.Error as error:
                print((Fore.RED if cm else "") + 
                      "Error populating order table for " + str(this_order_id) + ":" +
                      (Fore.RESET if cm else ""))
                print(error)

    #TODO: implement itamization and format order




    