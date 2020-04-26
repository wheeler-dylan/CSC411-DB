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
    import termcolor
    """example:
    print('\033[31m' + 'some red text')
    print('\033[39m') # and reset to default color
    """
except Exception as error:
    print(error)
    color_mode = False
else:
    colorama.init()
    from colorama import Fore, Back, Style
    color_mode = True
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
                       (Fore.GREEN if color_mode else "") + "exit" + (Fore.RESET if color_mode else "") + ": exit the program\n" +
                       (Fore.GREEN if color_mode else "") + "help" + (Fore.RESET if color_mode else "") + ": display commands list\n" +
                       (Fore.GREEN if color_mode else "") + "orders" + (Fore.RESET if color_mode else "") + ": view all orders made and amounts sold\n" +
                       (Fore.GREEN if color_mode else "") + "bestsellers" + (Fore.RESET if color_mode else "") + ": view best selling items by location\n" +
                       (Fore.GREEN if color_mode else "") + "employ" + (Fore.RESET if color_mode else "") + ": hire or fire a manager or associate\n" +
                       (Fore.GREEN if color_mode else "") + "pay" + (Fore.RESET if color_mode else "") + ": issue paychecks\n" +
                       (Fore.GREEN if color_mode else "") + "losses" + (Fore.RESET if color_mode else "") + ": check for lost or broken items\n" +
                       (Fore.GREEN if color_mode else "") + "suppliers" + (Fore.RESET if color_mode else "") + ": alter suppliers and shippers\n" +
                       (Fore.GREEN if color_mode else "") + "SQL" + (Fore.RESET if color_mode else "") + ": enter SQL query mode\n") 
    print(command_list)


    while(command != "exit"):

        command = get_cmd()

        if command == "exit":
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
                print((Fore.YELLOW if color_mode else ""))
                query = input("Enter a SQL Query:\n")
                print((Fore.RESET if color_mode else ""))

                if query == "exit": 
                    print("Now leaving SQL mode.")
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
        #End SQL mode

        #hire/fire mode
        elif command == "employ":
            print(bar)
            mode = ""
            while ((mode != "fire") or (mode != "hire")):
                print("Select from the following commmands:\n" + 
                      (Fore.GREEN if color_mode else "") + "exit" + (Fore.RESET if color_mode else "") + ": return to main menu\n" +
                      (Fore.GREEN if color_mode else "") + "hire" + (Fore.RESET if color_mode else "") + ": add a new employee\n" +
                      (Fore.GREEN if color_mode else "") + "fire" + (Fore.RESET if color_mode else "") + ": remove an employee\n")

                mode = get_cmd()

                if mode == "exit":
                    print("Exiting employ mode, type help to see commands.")
                    break

                elif mode == "fire":
                    fire_mode(conn, user)

                elif mode == "hire":
                    hire_mode(conn, user)

                else:
                    print("Invalid command entered.")

            print(bar)
        #end employ mode

        #view all orders
        elif command == "orders":
            print(bar)
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM orders ORDER BY date DESC").fetchall(), cursor.description)
            print(bar)
        #

        #view besetsellers
        elif command == "bestsellers":
            print(bar)
            store_ids = [i[0] for i in cursor.execute("SELECT id FROM stores;")]

            for each_store in store_ids:
                engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory WHERE store_id='" + str(each_store) +
                                                         "' ORDER BY sold_last_month DESC LIMIT 3").fetchall(), cursor.description)

            print(bar)
        #

        #view losses
        elif command == "losses":
            print(bar)
            engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory ORDER BY damaged_lost DESC LIMIT 3").fetchall(), cursor.description)
            print(bar)
        #

        else:
            print("Invalid command entered.")
            print(command_list)

        #end command switch block

    #end while command != exit

#end default_interface()



###############################################################################

def fire_mode(conn, user = None):
    """fire mode to remove an employee"""
    print((Fore.RED if color_mode else "") + "ATTENTION! " + (Fore.RESET if color_mode else "") + 
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

    if (fired_id == "cancel"):
        print("Exiting fire mode.\n")
        return

    else:
        if int(fired_id) in [i[0] for i in cursor.execute("SELECT id FROM employee")]:

            print((Fore.RED if color_mode else "") + "ATTENTION! " + (Fore.RESET if color_mode else "") +
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
        print("You may type " + (Fore.GREEN if color_mode else "") + "cancel" + (Fore.RESET if color_mode else "") + " at any time.\n" +
              "Enter new " + (Fore.CYAN if color_mode else "") + "employee ID" + (Fore.RESET if color_mode else "") +" or enter " +
              (Fore.GREEN if color_mode else "") + "random" + (Fore.RESET if color_mode else "") +
              " to generate a new unique id.") 

        new_id = get_cmd()

        if new_id == "cancel":
            print("Exiting hire mode.\n")
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
        input = get_cmd("Enter " + (Fore.CYAN if color_mode else "") + each_attribute + (Fore.RESET if color_mode else "") +
                        " or " + (Fore.GREEN if color_mode else "") + "NULL" + (Fore.RESET if color_mode else "") + 
                        " if unknown, or enter " + (Fore.GREEN if color_mode else "") + "cancel" + (Fore.RESET if color_mode else ""))
        if input == "cancel":
            print("Exiting hire mode.\n")
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #

    #get employee username
    username_found = False
    while not username_found:
        print("You may type " + (Fore.GREEN if color_mode else "") + "cancel" + (Fore.RESET if color_mode else "") + " at any time.\n" +
              "Enter new employee " + (Fore.CYAN if color_mode else "") + "username" + (Fore.RESET if color_mode else "") +
              " or enter " + (Fore.GREEN if color_mode else "") + "random" + (Fore.RESET if color_mode else "") +
              " to generate a new unique username.") 

        new_username = get_cmd()

        if new_username == "cancel":
            print("Exiting hire mode.\n")
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
        input = get_cmd("Enter " + (Fore.CYAN if color_mode else "") + each_attribute + (Fore.RESET if color_mode else "") +
                        " or " + (Fore.GREEN if color_mode else "") + "NULL" + (Fore.RESET if color_mode else "") + 
                        " if unknown, or enter " + (Fore.GREEN if color_mode else "") + "cancel" + (Fore.RESET if color_mode else ""))

        if input == "cancel":
            print("Exiting hire mode.\n")
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #


    #get employee database access level
    while input not in ["admin", "manager", "associate"]:
        input = get_cmd("Enter database permission level from:\n" +
                        (Fore.GREEN if color_mode else "") + "admin" + (Fore.RESET if color_mode else "") + "\n" +
                        (Fore.GREEN if color_mode else "") + "manager" + (Fore.RESET if color_mode else "") + "\n" +
                        (Fore.GREEN if color_mode else "") + "associate" + (Fore.RESET if color_mode else "") + "\n")

        if input == "cancel":
            print("Exiting hire mode.\n")
            return

    #
    new_values = new_values + "'" + str(input) + "', "


    next_attributes = ["start date", "end date", "vacation days", "contract ID"]

    for each_attribute in next_attributes:
        input = get_cmd("Enter " + (Fore.CYAN if color_mode else "") + each_attribute + (Fore.RESET if color_mode else "") +
                        " or " + (Fore.GREEN if color_mode else "") + "NULL" + (Fore.RESET if color_mode else "") + 
                        " if unknown, or enter " + (Fore.GREEN if color_mode else "") + "cancel" + (Fore.RESET if color_mode else ""))  
            
        if input == "cancel":
            print("Exiting hire mode.\n")
            return
        else:
            new_values = new_values + "'" + str(input) + "', "
    #

    #remove last comma
    new_values = new_values[:-2]

    print((Back.CYAN if color_mode else "") + "Adding new employee to database..." + (Back.RESET if color_mode else ""))

    try:
        cursor.execute("INSERT INTO employee VALUES (" + new_values + ");")
    except sqlite3.Error as error:
        print((Fore.RED if color_mode else "") + "ERROR: " + (Fore.RESET if color_mode else "") +
              "SQL error found in default.py > hire_mode():\n" + str(error))
    else:
        print("New employee added!")
        engine.print_cursor_fetch(cursor.execute("SELECT * FROM employee WHERE id='" + str(new_id) + "'").fetchall(), cursor.description)


    print("Exiting hire mode.\n")
#End hire mode



###############################################################################

#