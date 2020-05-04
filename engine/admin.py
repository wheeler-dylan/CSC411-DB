#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
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

def admin_interface(conn, user):
    cursor = conn.cursor()

    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory").fetchall(), cursor.description) #debugging
    print()

    bar = str("\n" + ("-" * 25) + "\n")

    command = ""
    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       (Fore.GREEN if cm else "") + "exit" + (Fore.RESET if cm else "") + ": exit the program\n" +
                       (Fore.GREEN if cm else "") + "help" + (Fore.RESET if cm else "") + ": display commands list\n" +
                       (Fore.GREEN if cm else "") + "orders" + (Fore.RESET if cm else "") + ": view all orders made and amounts sold\n" +
                       (Fore.GREEN if cm else "") + "bestsellers" + (Fore.RESET if cm else "") + ": view best selling items by location\n" +
                       (Fore.GREEN if cm else "") + "employ" + (Fore.RESET if cm else "") + ": hire or fire a manager or associate\n" +
                       #(Fore.GREEN if cm else "") + "pay" + (Fore.RESET if cm else "") + ": issue paychecks\n" +
                       (Fore.GREEN if cm else "") + "losses" + (Fore.RESET if cm else "") + ": check for lost or broken items\n" +
                       (Fore.GREEN if cm else "") + "suppliers" + (Fore.RESET if cm else "") + ": alter suppliers and shippers\n" +
                       (Fore.GREEN if cm else "") + "SQL" + (Fore.RESET if cm else "") + ": enter SQL query mode\n" +
                       "") 
    print(command_list)


    while(command != "exit"):

        command = get_cmd()

        if (engine.quit(command)):
            continue

        elif command == "help":
            print(command_list)
            continue

        #SQL MODE
        elif command == "SQL":
            print(bar)
            print("Now entering SQL mode, all other commands are now invalid.\n" + 
                  "enter 'exit' to leave SQL mode.\n")

            query = ""
            while query != "exit":
                print((Fore.YELLOW if cm else ""))
                query = input("Enter a SQL Query:\n")
                print((Fore.RESET if cm else ""))

                if engine.quit(query, "Now leaving SQL mode."): 
                    print(command_list)
                    continue
            
                try:
                    cursor.execute(query)

                except sqlite3.Error as error:
                    print("Error executive SQL query:\n" + str(error) + "\n" +
                          "Use the command 'exit' to leave SQL mode.\n")

                else:
                    engine.print_cursor_fetch(cursor.fetchall(), cursor.description)

            #end while query != exit
            print(bar)
            continue
        #End SQL mode

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

        #view all orders
        elif command == "orders":
            print(bar)
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM orders ORDER BY date DESC").fetchall(), cursor.description)
            print(bar)
            continue
        #

        #view besetsellers
        elif command == "bestsellers":
            print(bar)

            store_ids = [i[0] for i in cursor.execute("SELECT id FROM stores;")]
            for each_store in store_ids:
                engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(each_store) +
                                                         "' ORDER BY sold_last_month DESC LIMIT 10").fetchall(), cursor.description)
                print()
            print(bar)
            continue
        #

        #view losses
        elif command == "losses":
            print(bar)

            store_ids = [i[0] for i in cursor.execute("SELECT id FROM stores;")]
            for each_store in store_ids:
                engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(each_store) +
                                                         "' ORDER BY damaged_lost DESC LIMIT 10").fetchall(), cursor.description)            
                print()
            print(bar)
            continue
        #

        elif command == "suppliers":
            print(bar)
            edit_suppliers(conn, user)
            print(bar)
            continue

        else:
            print("Invalid command entered.")
            print(command_list)

        #end command switch block

    #end while command != exit

#end default_interface()



###############################################################################

def fire_mode(conn, user = None):
    """fire mode to remove an employee"""
    print((Fore.RED if cm else "") + "ATTENTION! " + (Fore.RESET if cm else "") + 
          "You are entering fire mode, this will PERMANENTLY remove employees from the database.\n")

    cursor = conn.cursor()

    confirm = get_cmd("Enter YES to continue, any other input will cancel.")

    if (confirm != "YES"):
        print("Exiting fire mode.\n")
        return
    
    attributes = str("id, first_name, last_name, store_id, phone_number, username, job_title, contract_id")
    engine.print_cursor_fetch(cursor.execute("SELECT " + attributes + " FROM employee").fetchall(), cursor.description)
    print()

    fired_id = get_cmd("Enter the employee ID to fire employee, or type cancel..")

    if engine.quit(fired_id, "Exiting fire mode."):
        return

    else:
        if int(fired_id) in [i[0] for i in cursor.execute("SELECT id FROM employee")]:

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
                print("SQL Error found in admin.py > fire_mode()\n" + error)
            else:
                print("Employee removed from database.\n")
                engine.print_cursor_fetch(cursor.execute("SELECT " + attributes + " FROM employee").fetchall(), cursor.description)
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

    next_attributes = ["first name", "last name", "store ID", 
                       "ssn", "phone number", "street number", "street name", "city", "zip"]

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


    #get employee database access level
    while input not in ["admin", "manager", "associate"]:
        input = get_cmd("Enter database permission level from:\n" +
                        (Fore.GREEN if cm else "") + "admin" + (Fore.RESET if cm else "") + "\n" +
                        (Fore.GREEN if cm else "") + "manager" + (Fore.RESET if cm else "") + "\n" +
                        (Fore.GREEN if cm else "") + "associate" + (Fore.RESET if cm else "") + "\n")

        if engine.quit(input,"Exiting hire mode."):
            return

    #
    new_values = new_values + "'" + str(input) + "', "


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



def edit_suppliers(conn, user):
    cursor = conn.cursor()

    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       (Fore.GREEN if cm else "") + "supp" + (Fore.RESET if cm else "") + ": view suppliers\n" +
                       (Fore.GREEN if cm else "") + "add_supp" + (Fore.RESET if cm else "") + ": add a new supplier\n" +
                       (Fore.GREEN if cm else "") + "remove_supp" + (Fore.RESET if cm else "") + ": remove a supplier\n" +
                       (Fore.GREEN if cm else "") + "ship" + (Fore.RESET if cm else "") + ": view shippers\n" +
                       (Fore.GREEN if cm else "") + "add_ship" + (Fore.RESET if cm else "") + ": add a new shipper\n" +
                       (Fore.GREEN if cm else "") + "remove_ship" + (Fore.RESET if cm else "") + ": remove a shipper\n" +
                       "") 

    command = ""

    while(command != "exit"):
        print(command_list)

        command = get_cmd()

        if (engine.quit(command)):
            continue

        elif command == "help":
            print(command_list)
            print()
            continue

        elif command == "supp":
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM supplier").fetchall(), cursor.description)
            print()
            continue
        #

        elif command == "add_supp":
            
            new_values = ""
            
            #get supplier ID
            id_found = False
            while not id_found:
                print("You may type " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + " at any time.\n" +
                      "Enter new " + (Fore.CYAN if cm else "") + "supplier ID" + (Fore.RESET if cm else "") +" or enter " +
                      (Fore.GREEN if cm else "") + "random" + (Fore.RESET if cm else "") +
                      " to generate a new unique id.") 

                new_id = get_cmd()

                if engine.quit(new_id, "Exiting suppliers mode.\n"):
                    return

                elif new_id == "random":
                    while not id_found:
                        new_id = random.randint(10001, 99998)
                        if int(new_id) in [i[0] for i in cursor.execute("SELECT id FROM supplier")]:
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
                        if int(new_id) in [i[0] for i in cursor.execute("SELECT id FROM supplier")]:
                            print("ALERT: this ID already exists.\n")
                        else: 
                            id_found = True

            #end get employee id

            new_values = new_values + "'" + str(new_id) + "', "


            """from /schemas/supplier.csv:
                id;name;address_number;address_street;address_city;address_zip;email;phone_number
                int;varchar(255);int;varchar(255);varchar(255);int;varchar(255);int
            """

            next_attributes = ["Name", "Street Number", "Street", "City", "Zip", "Contact Email", "Phone number"]

            for each_attribute in next_attributes:
                input = get_cmd("Enter " + (Fore.CYAN if cm else "") + each_attribute + (Fore.RESET if cm else "") +
                                " or " + (Fore.GREEN if cm else "") + "NULL" + (Fore.RESET if cm else "") + 
                                " if unknown, or enter " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else ""))

                if engine.quit(input,"Exiting suppliers mode."):
                    return
                else:
                    new_values = new_values + "'" + str(input) + "', "
            #

            #remove last comma
            new_values = new_values[:-2]

            #add to database
            print((Back.CYAN if cm else "") + "Adding new supplier to database..." + (Back.RESET if cm else ""))

            try:
                cursor.execute("INSERT INTO supplier VALUES (" + new_values + ");")
            except sqlite3.Error as error:
                print((Fore.RED if cm else "") + "ERROR: " + (Fore.RESET if cm else "") +
                      "SQL error found in default.py > hire_mode():\n" + str(error))
            else:
                print("New supplier added!")
                engine.print_cursor_fetch(cursor.execute("SELECT * FROM supplier WHERE id='" + str(new_id) + "'").fetchall(), cursor.description)

            continue
        #end command == add_supp
        
        
        
        elif command == "remove_supp":

            engine.print_cursor_fetch(cursor.execute("SELECT * FROM supplier").fetchall(), cursor.description)
            print()

            removed_id = get_cmd("Enter the " +(Fore.RED if cm else "") + "Supplier ID " + (Fore.RESET if cm else "") +" of the supplier to remove")

            if engine.quit(removed_id, "Exiting suppliers mode."):
                return

            else:
                if int(removed_id) in [i[0] for i in cursor.execute("SELECT id FROM supplier")]:

                    print((Fore.RED if cm else "") + "ATTENTION! " + (Fore.RESET if cm else "") +
                          "You about to remove the following supplier from the database:")
                    engine.print_cursor_fetch(cursor.execute("SELECT * FROM supplier WHERE id='" + str(removed_id) + "'").fetchall(), cursor.description)
                    print()

                    confirm = get_cmd("Enter YES to continue, any other input will cancel.")

                    if (confirm != "YES"):
                        print("Exiting suppliers mode.\n")
                        return

                    try:
                        cursor.execute("DELETE FROM supplier WHERE id='" + str(removed_id) + "'")
                    except sqlite3.Error as error:
                        print("SQL Error found in admin.py > edit_suppliers()\n" + error)
                    else:
                        print("Supplier removed from database.\n")
                        engine.print_cursor_fetch(cursor.execute("SELECT * FROM supplier").fetchall(), cursor.description)
                        print()

                else:
                    print("Supplier ID not found.\n")
            continue

        elif command == "ship":
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM shippers").fetchall(), cursor.description)
            print()
            continue

        elif command == "add_ship":

            new_values = ""
            
            #get supplier ID
            id_found = False
            while not id_found:
                print("You may type " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else "") + " at any time.\n" +
                      "Enter new " + (Fore.CYAN if cm else "") + "shipper ID" + (Fore.RESET if cm else "") +" or enter " +
                      (Fore.GREEN if cm else "") + "random" + (Fore.RESET if cm else "") +
                      " to generate a new unique id.") 

                new_id = get_cmd()

                if engine.quit(new_id, "Exiting suppliers mode.\n"):
                    return

                elif new_id == "random":
                    while not id_found:
                        new_id = random.randint(10001, 99998)
                        if int(new_id) in [i[0] for i in cursor.execute("SELECT id FROM shippers")]:
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
                        if int(new_id) in [i[0] for i in cursor.execute("SELECT id FROM shippers")]:
                            print("ALERT: this ID already exists.\n")
                        else: 
                            id_found = True

            #end get employee id

            new_values = new_values + "'" + str(new_id) + "', "


            """from /schemas/supplier.csv:
                id;shipper_name;shipper_account_number;phone_number;email;address_number;address_street_name;address_city;address_zip_code
                int;varchar(256);int;int;varchar(256);int;varchar(256);varchar(256);int;int
            """

            next_attributes = ["Name", "Account Number", "Phone number", "Contact Email", "Street Number", "Street", "City", "Zip"]

            for each_attribute in next_attributes:
                input = get_cmd("Enter " + (Fore.CYAN if cm else "") + each_attribute + (Fore.RESET if cm else "") +
                                " or " + (Fore.GREEN if cm else "") + "NULL" + (Fore.RESET if cm else "") + 
                                " if unknown, or enter " + (Fore.GREEN if cm else "") + "cancel" + (Fore.RESET if cm else ""))

                if engine.quit(input,"Exiting suppliers mode."):
                    return
                else:
                    new_values = new_values + "'" + str(input) + "', "
            #

            #remove last comma
            new_values = new_values[:-2]

            #add to database
            print((Back.CYAN if cm else "") + "Adding new shipper to database..." + (Back.RESET if cm else ""))

            try:
                cursor.execute("INSERT INTO shippers VALUES (" + new_values + ");")
            except sqlite3.Error as error:
                print((Fore.RED if cm else "") + "ERROR: " + (Fore.RESET if cm else "") +
                      "SQL error found in default.py > hire_mode():\n" + str(error))
            else:
                print("New shipper added!")
                engine.print_cursor_fetch(cursor.execute("SELECT * FROM shippers WHERE id='" + str(new_id) + "'").fetchall(), cursor.description)

            continue
        #end command == add_ship

        elif command == "remove_ship":

            engine.print_cursor_fetch(cursor.execute("SELECT * FROM shippers").fetchall(), cursor.description)
            print()

            removed_id = get_cmd("Enter the " +(Fore.RED if cm else "") + "Shipper ID " + (Fore.RESET if cm else "") +" of the shipper to remove")

            if engine.quit(removed_id, "Exiting suppliers mode."):
                return

            else:
                if int(removed_id) in [i[0] for i in cursor.execute("SELECT id FROM shippers")]:

                    print((Fore.RED if cm else "") + "ATTENTION! " + (Fore.RESET if cm else "") +
                          "You about to remove the following shipper from the database:")
                    engine.print_cursor_fetch(cursor.execute("SELECT * FROM shippers WHERE id='" + str(removed_id) + "'").fetchall(), cursor.description)
                    print()

                    confirm = get_cmd("Enter YES to continue, any other input will cancel.")

                    if (confirm != "YES"):
                        print("Exiting suppliers mode.\n")
                        return

                    try:
                        cursor.execute("DELETE FROM shippers WHERE id='" + str(removed_id) + "'")
                    except sqlite3.Error as error:
                        print("SQL Error found in admin.py > edit_suppliers()\n" + error)
                    else:
                        print("Shipper removed from database.\n")
                        engine.print_cursor_fetch(cursor.execute("SELECT * FROM shippers").fetchall(), cursor.description)
                        print()

                else:
                    print("Shipper ID not found.\n")

            continue
#end edit_suppliers


