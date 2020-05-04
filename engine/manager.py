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


        elif command == "bestsellers":
            print(bar)

            engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(user.store_id) +
                                                     "' ORDER BY sold_last_month DESC LIMIT 10").fetchall(), cursor.description)

            print(bar)
            continue
        #


        #hire/fire mode
        elif command == "employ":
            print(bar)
            mode = ""
            while ((mode != "fire") or (mode != "hire")):
                print("Select from the following commmands:\n" + 
                      (Fore.GREEN if cm else "") + "exit" + (Fore.RESET if cm else "") + ": return to main menu\n" +
                      (Fore.GREEN if cm else "") + "hire" + (Fore.RESET if cm else "") + ": add a new employee\n" +
                      (Fore.GREEN if cm else "") + "fire" + (Fore.RESET if cm else "") + ": remove an employee\n")

                mode = get_cmd()

                if engine.quit(mode, "Exiting employ mode, type help to see commands."):
                    break

                elif mode == "fire":
                    fire_mode(conn, user)

                elif mode == "hire":
                    hire_mode(conn, user)

                else:
                    print("Invalid command entered.")

            print(bar)
            continue
        #end employ mode


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

            order.reorder(conn, user)

            continue
        #end command = reorder

        else:
            print("Error, invalid command entered.")
            continue

    #End while

#End order_mode()



###############################################################################

def fire_mode(conn, user):
    """fire mode to remove an employee"""
    print((Fore.RED if cm else "") + "ATTENTION! " + (Fore.RESET if cm else "") + 
          "You are entering fire mode, this will PERMANENTLY remove employees from the database.\n")

    cursor = conn.cursor()

    confirm = get_cmd("Enter YES to continue, any other input will cancel.")

    if (confirm != "YES"):
        print("Exiting fire mode.\n")
        return
    
    attributes = str("id, first_name, last_name, store_id, phone_number, username, job_title, contract_id")
    engine.print_cursor_fetch(cursor.execute("SELECT " + attributes + " FROM employee WHERE " +
                                             "db_permission_level = 'associate' AND " + 
                                             "store_id = '" + str(user.store_id) + "'").fetchall(), cursor.description)
    print()

    fired_id = get_cmd("Enter the employee ID to fire employee, or type cancel..")

    if engine.quit(fired_id, "Exiting fire mode."):
        return

    else:
        if int(fired_id) in [i[0] for i in cursor.execute("SELECT id FROM employee WHERE " +
                                                          "db_permission_level = 'associate' AND " + 
                                                          "store_id = '" + str(user.store_id) + "'")]:

            print((Fore.RED if cm else "") + "ATTENTION! " + (Fore.RESET if cm else "") +
                  "You about to remove the following employee from the database:")
            engine.print_cursor_fetch(cursor.execute("SELECT " + attributes + " FROM employee WHERE id='" + str(fired_id) + "'").fetchall(), cursor.description)
            print()

            confirm = get_cmd("Enter YES to continue, any other input will cancel.")

            if (confirm != "YES"):
                print("Exiting fire mode.\n")
                return

            try:
                cursor.execute("DELETE FROM employee WHERE id='" + str(fired_id) + "'")
            except sqlite3.Error as error:
                print("SQL Error found in default.py > fire_mode()\n" + error)
            else:
                print("Employee removed from database.\n")
                engine.print_cursor_fetch(cursor.execute("SELECT " + attributes + 
                                                         " FROM employee WHERE store_id = '" + user.store_id + "'").fetchall(), cursor.description)
                print()

        else:
            print("Employee ID not found.\n")

    print("Exiting fire mode.\n")
#End fire mode



###############################################################################

def hire_mode(conn, user = None):
    """guides an admin to adding a new user to the database"""
    print("You are entering hire mode, this will add employees to the database.\n")

    cursor = conn.cursor()


    new_values = ""

    """from /schemas/employee.csv:
        id;first_name;last_name;store_id;
        ssn;phone_number;address_number;address_street;address_city;address_zip;
        username;password;job_title;db_permission_level;
        start_date;end_date;vacation_days_remaining;contract_id
    """

    #get employee ID
    id_found = False
    while not id_found:
        print("You may type " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + " at any time.\n" +
              "Enter new " + (Fore.CYAN if cm else "") + "employee ID" + (Fore.RESET if cm else "") +" or enter " +
              (Fore.GREEN if cm else "") + "random" + (Fore.RESET if cm else "") +
              " to generate a new unique id.") 

        new_id = get_cmd()

        if engine.quit(new_id, "Exiting hire mode.\n"):
            return

        elif new_id == "random":
            while not id_found:
                new_id = random.randint(10001, 99998)
                if int(new_id) in [i[0] for i in cursor.execute("SELECT id FROM employee")]:
                    continue
                else:
                    id_found = True

        else:
            try:
                new_id = int(new_id)
            
            except:
                print("ID must be an integer")
                continue
            
            else:
                if int(new_id) in [i[0] for i in cursor.execute("SELECT id FROM employee")]:
                    print("ALERT: this ID already exists.\n")
                else: 
                    id_found = True

    #end get employee id
    new_values = new_values + "'" + str(new_id) + "', "

    """from /schemas/employee.csv:
        id;first_name;last_name;store_id;
        ssn;phone_number;address_number;address_street;address_city;address_zip;
        username;password;job_title;db_permission_level;
        start_date;end_date;vacation_days_remaining;contract_id
    """

    next_attributes = ["first name", "last name"]

    for each_attribute in next_attributes:
        input = get_cmd("Enter " + (Fore.CYAN if cm else "") + each_attribute + (Fore.RESET if cm else "") +
                        " or " + (Fore.GREEN if cm else "") + "NULL" + (Fore.RESET if cm else "") + 
                        " if unknown, or enter " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else ""))
        if engine.quit(input,"Exiting hire mode."):
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #

    new_values = new_values + "'" + str(user.store_id) + "', "

    next_attributes = ["ssn", "phone number", "street number", "street name", "city", "zip"]

    for each_attribute in next_attributes:
        input = get_cmd("Enter " + (Fore.CYAN if cm else "") + each_attribute + (Fore.RESET if cm else "") +
                        " or " + (Fore.GREEN if cm else "") + "NULL" + (Fore.RESET if cm else "") + 
                        " if unknown, or enter " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else ""))
        if engine.quit(input,"Exiting hire mode."):
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #

    #get employee username
    username_found = False
    while not username_found:
        print("You may type " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + " at any time.\n" +
              "Enter new employee " + (Fore.CYAN if cm else "") + "username" + (Fore.RESET if cm else "") +
              " or enter " + (Fore.GREEN if cm else "") + "random" + (Fore.RESET if cm else "") +
              " to generate a new unique username.") 

        new_username = get_cmd()

        if engine.quit(new_username,"Exiting hire mode."):
            return

        elif new_username == "random":
            while not username_found:
                new_username = random.randint(10001, 99998)
                if str(new_username) in [i[0] for i in cursor.execute("SELECT username FROM employee")]:
                    continue
                else:
                    username_found = True

        else:
                if str(new_username) in [i[0] for i in cursor.execute("SELECT username FROM employee")]:
                    print("ALERT: this username already exists.\n")
                else: 
                    username_found = True

    #end get employee username
    new_values = new_values + "'" + str(new_username) + "', "

    """from /schemas/employee.csv:
        id;first_name;last_name;store_id;
        ssn;phone_number;address_number;address_street;address_city;address_zip;
        username;password;job_title;db_permission_level;
        start_date;end_date;vacation_days_remaining;contract_id
    """

    next_attributes = ["password", "job title"]

    for each_attribute in next_attributes:
        input = get_cmd("Enter " + (Fore.CYAN if cm else "") + each_attribute + (Fore.RESET if cm else "") +
                        " or " + (Fore.GREEN if cm else "") + "NULL" + (Fore.RESET if cm else "") + 
                        " if unknown, or enter " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else ""))

        if engine.quit(input,"Exiting hire mode."):
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #


    new_values = new_values + "'associate', "


    next_attributes = ["start date", "end date", "vacation days", "contract ID"]

    for each_attribute in next_attributes:
        input = get_cmd("Enter " + (Fore.CYAN if cm else "") + each_attribute + (Fore.RESET if cm else "") +
                        " or " + (Fore.GREEN if cm else "") + "NULL" + (Fore.RESET if cm else "") + 
                        " if unknown, or enter " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else ""))  
            
        if engine.quit(input,"Exiting hire mode."):
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #

    #remove last comma
    new_values = new_values[:-2]

    print((Back.CYAN if cm else "") + "Adding new employee to database..." + (Back.RESET if cm else ""))

    try:
        cursor.execute("INSERT INTO employee VALUES (" + new_values + ");")
    except sqlite3.Error as error:
        print((Fore.RED if cm else "") + "ERROR: " + (Fore.RESET if cm else "") +
              "SQL error found in default.py > hire_mode():\n" + str(error))
    else:
        print("New employee added!")
        engine.print_cursor_fetch(cursor.execute("SELECT * FROM employee WHERE id='" + str(new_id) + "'").fetchall(), cursor.description)


    print("Exiting hire mode.\n")
#End hire mode



###############################################################################

#