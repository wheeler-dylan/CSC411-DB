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
                    " of the item you'd like to order.")

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
                            " of the item you'd like to order.")

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

#end reorder()




def restock(conn, user):
    """restock items in inventory"""
    cursor = conn.cursor()

    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                             "' ORDER BY stock ASC").fetchall(), cursor.description)

    #get inventory id for items to add
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
    restock_id = int(input)

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
            restock_quantity = int(input)
            break 
    #end get quantity

    restock_quantity = int( int(restock_quantity) + int(engine.get_cell(conn, "stock", "inventory", "id", restock_id)) )

    try:
        query = str("UPDATE inventory SET stock = '" + str(restock_quantity) + 
                    "' WHERE id = '" + str(restock_id) + "';") 
        cursor.execute(query)

    except sqlite3.Error as error:
        print((Fore.RED if cm else "") + 
                "Error restocking inventory item " + str(restock_id) + ":" +
                (Fore.RESET if cm else ""))
        print(query)
        print(error)

    else:
        print("Successfully added stock.")
        engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                                 "' ORDER BY stock ASC").fetchall(), cursor.description)
#end restock()




def checkout(conn, user):
    cursor = conn.cursor()
    cart = []
    grand_total = 0.00

    while True:
        #get inventory id for items to order
        input = get_cmd("Enter the " + 
                        (Fore.CYAN if cm else "") + "Inventory ID" + (Fore.RESET if cm else "") + 
                        " of the item you'd add.\n" +
                        "Enter " + 
                        (Fore.CYAN if cm else "") + "cancel" + (Fore.RESET if cm else "") + 
                        " to exit.\n" +
                        "Enter " + 
                        (Fore.CYAN if cm else "") + "done" + (Fore.RESET if cm else "") + 
                        " when complete.")

        if (engine.quit(input, "Exiting checkout mode.")):
            input = "_BREAKLOOP_"
            break

        elif input == "done":
            break

        elif int(input) not in [i[0] for i in cursor.execute("SELECT id FROM inventory WHERE " +
                                                             "id = '" + input + "';").fetchall()]:
            print((Fore.RED if cm else "") + 
                  "Error: inventory item " + str(input) + " not found." +
                  (Fore.RESET if cm else ""))
            continue #got to top of input loop

        else: #not done, not exit, and inventory item is found; add to list
            cart.append(input)
            print("Item " + 
                  (Fore.GREEN if cm else "") + input + (Fore.RESET if cm else "") + 
                  " added to purchase!")

    if input == "_BREAKLOOP_": #if canceling purchase
        return #break out of checkout mode
    #end while True

    #get customer info
    input = get_cmd("Would the customer like to use their membership ID? Enter the " + 
                    (Fore.CYAN if cm else "") + "Customer ID" + (Fore.RESET if cm else "") + 
                    " or enter " +
                    (Fore.CYAN if cm else "") + "no" + (Fore.RESET if cm else "") + ".")

    if (engine.quit(input, "Exiting checkout mode.")):
        return
    elif (input.lower() == "no"):
        customer_id = "NULL"
    else:
        customer_id = input
        while int(input) not in [i[0] for i in cursor.execute("SELECT id FROM customer WHERE " +
                                                "id = '" + input + "';").fetchall()]: 
            input = get_cmd("Customer ID not found, please re-enter Customer ID, or type "+ 
                            (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + 
                            " to cancel.") 
            customer_id = input
            if (engine.quit(input), "Not using Customer ID, get CC info."):
                customer_id = "NULL"
                break
    #end get customer id

    #get cc info
    if customer_id != "NULL":
        input = get_cmd("Would the customer like to use new CC or charge or their card on file? Enter the " + 
                        (Fore.CYAN if cm else "") + "card" + (Fore.RESET if cm else "") + 
                        " or enter " +
                        (Fore.CYAN if cm else "") + "account" + (Fore.RESET if cm else "") + ".")
        if (engine.quit(input, "Exiting checkout mode.")):
            return

    if ((customer_id == "NULL") or (input == "card")):
        input = get_cmd("Enter the customer's " + 
                        (Fore.CYAN if cm else "") + "CC number" + (Fore.RESET if cm else "") + ".")
        if (engine.quit(input, "Exiting checkout mode.")):
            return
        customer_cc = str(input)

        input = get_cmd("Enter the customer's " + 
                        (Fore.CYAN if cm else "") + "CC expiration date" + (Fore.RESET if cm else "") + ".")
        if (engine.quit(input, "Exiting checkout mode.")):
            return
        customer_cc_exp = str(input)

    elif input == "account": 
        customer_cc = str(engine.get_cell(conn, "card_number", "customer", "id", customer_id))
        customer_cc_exp = str(engine.get_cell(conn, "card_exp", "customer", "id", customer_id))

    else:
        print((Fore.RED if cm else "") + 
                "Error inputing CC information. CC set to NULL, contact manager." +
                (Fore.RESET if cm else "") )
        customer_cc = str("NULL")
        customer_cc_exp = str("NULL")
    #end get CC info

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
        #add each item in cart to itemized table
        for each_item_id in cart:
            try:
                this_row_id = str(random.randint(11111111, 99999999))   #get random id for item row
                this_row_category = str(engine.get_cell(conn, "category", "inventory", "id", each_item_id))   #get category from inventory table
                this_row_item_id = str(engine.get_cell(conn, "item_id", "inventory", "id", each_item_id))     #get item_id from inventory table
                this_row_price = str(engine.get_cell(conn, "price", this_row_category, "id", this_row_item_id))       #get quantity to be ordered

                query = str("INSERT INTO " + item_id + " VALUES ('401" +
                            str(this_row_id) + "', '" +    
                            str(this_row_category) + "', '" +  
                            str(this_row_item_id) + "', '" +  
                            str("1") + "', '" +      
                            str(this_row_price) +
                            "');")

                print(query) #debugging
                cursor.execute(query)

            except sqlite3.Error as error:
                print((Fore.RED if cm else "") + 
                        "Error populating itemization table for " + str(item_id) + ":" +
                        (Fore.RESET if cm else ""))
                print(query)
                print(error)

            else: 
                grand_total = float(float(grand_total) + float(this_row_price))
        #end adding to table

        #add purchase to purchases table
        try:
            #get unique order id
            while True:
                this_purchase_id = random.randint(11111111, 99999999)
                if this_purchase_id in [i[0] for i in cursor.execute("SELECT id FROM purchases;")]:
                    continue #if exists, try again
                else:
                    break #if unique, move on
            #

            """
            From pruchases schema:
            id;customer_id;store_id;cc_number;cc_expiration;itemization_id;grand_total;date
            int;int;int;int;date;varchar(255);float(12,2);date
            """

            query = str("INSERT INTO purchases VALUES ('" +
                        str(this_purchase_id) + "', '" +    
                        str(customer_id) + "', '" + #TODO: get customer ID
                        str(user.store_id) + "', '" + 
                        str(customer_cc) + "', '" +
                        str(customer_cc_exp) + "', '" +      
                        str(item_id) + "', '" +
                        str(grand_total) + "', '" + 
                        str(date.today()) +  
                        "');")

            for each_item in cart:
                print("Buying item " + 
                      str(engine.get_cell(conn, "name", "inventory", "id", each_item)) +
                      "...")
            print(query)    #debugging
            cursor.execute(query)

        except sqlite3.Error as error:
            print((Fore.RED if cm else "") + 
                  "Error populating puchases table for " + str(this_purchase_id) + ":" +
                  (Fore.RESET if cm else ""))
            print(error)

    print("\nGrand total for the purchase is:\n" + (Fore.GREEN if cm else "") + 
          "$" + str(round(grand_total,2)) + (Fore.RESET if cm else "") + "\n")
#end checkout()