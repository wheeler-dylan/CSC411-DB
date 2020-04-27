#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 02 15
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

#uses tutorial found at https://www.geeksforgeeks.org/sql-using-python/
"""
SQLite3 uses the following cycle to execute SQL commands:
    connection = sqlite3.connect("BryanElectronics.db")     //establishes DB file
    crsr = connection.cursor()  //build cursor to SQL interpretter, commands entered at this point
    sql_command = "string"      //write a SQL command and store as a string
    crsr.execute(sql_command)   //execute the SQL command
    connection.commit()         //saves changes to the database
    connection.close()          //closes connection
"""




import sys
sys.path.append("./schemas")
sys.path.append("./class_definitions")
sys.path.append("./engine")
import schemas
import foreign_keys
import user
import engine
from engine import get_cmd
import admin
import manager

#use formatted text colors if library is available
try:
    import colorama
except Exception as error:
    print("Color library not found.")
    print(error)
    print("In your python command line window, try entering:")
    print("\tpip install colorama")
    cm = False
else:
    colorama.init()
    from colorama import Fore, Back, Style
    cm = True
#

#filename to store db
database_filename = "BryanElectronics.db"

#establish connection to db in order to execute sql commands
import sqlite3 
connection = sqlite3.connect(database_filename) 
cursor = connection.cursor() 


###################### DEBUGGING MODE #######################
debugging = True

import os
if debugging:
    
    debugging_username = "BrownM"
    debugging_password = "012346"
    debugging_usertype = "manager"

    engine.debugging_mode(connection, database_filename)

    connection = sqlite3.connect(database_filename) 
    cursor = connection.cursor() 
#################### END DEBUGGING MODE ####################





#enter username and password
username = ""
password = ""
active_user = None
print( (Back.MAGENTA) if cm else "", end="")
print("Welcome to Bryan Electronics Database Management System!")
print( (Back.RESET) if cm else "", end="")

#find username
user_found = False
user_type = ""

if debugging:
    username = debugging_username
    user_type = debugging_usertype
    user_found = True
#

while not user_found:
    username = get_cmd("Please enter your username:\n")
    
    #search default users
    if username in user.default_users.keys():
        user_found = True
        user_type = "default"
        continue

    #search employees
    #search python list of usernames from employee, generated by SQL query
    if username in [i[0] for i in cursor.execute("SELECT username FROM employee;").fetchall()]: 
        user_found = True
        user_type = str(cursor.execute("SELECT db_permission_level FROM employee WHERE username='" + username + "';").fetchall()[0][0])
        print(user_type) #debugging
        continue

    #search customers
    #search python list of usernames from employee, generated by SQL query
    if username in [i[0] for i in cursor.execute("SELECT username FROM customer;").fetchall()]: 
        user_found = True
        user_type = "customer"
        continue

    print("Username not found.")
#


#after username has been found, enter password
password_found = False

if debugging:
    password = debugging_password
    password_found = True
    get_cmd("DEBUGGING MODE: Press ENTER to continue...")
#

while not password_found:
    password = get_cmd("Please enter your password:\n")

    if user_type == "default":
        if password == user.default_users[username].password:
            password_found = True
            continue

    elif user_type in ["admin", "manager", "associate"]:
        if password in [i[0] for i in cursor.execute("SELECT password FROM employee WHERE username='" + str(username) + "';")]:
            password_found = True
            continue

    elif user_type == "customer":
        if password in [i[0] for i in cursor.execute("SELECT password FROM customer WHERE username='" + str(username) + "';")]:
            password_found = True
            continue
    else:
        print("Critical error in main.py: invalid user_type.")
        
    print("Password is incorrect.")
#

#after password is found
#print("Thank you!")

engine.clear_screen()

print("Welcome " + str(username) + "!")

#if admin user
if user_type in ["default", "admin"]:
    active_user = user.default_users[username]
    admin.admin_interface(connection, active_user) #open interface
#

#if manager
elif user_type == "manager":
    #configure user settings
    this_id = int(engine.get_cell(connection, "id", "employee", "username", username))
    active_user = user.User("manager", this_id, "manager", username, password)

    this_first_name = str(engine.get_cell(connection, "first_name", "employee", "username", username))
    this_last_name = str(engine.get_cell(connection, "last_name", "employee", "username", username))
    this_store_id = int(engine.get_cell(connection, "store_id", "employee", "username", username))
    active_user.configure_employee(this_first_name, this_last_name, this_store_id)

    #open interface
    manager.manager_interface(connection, active_user)
#

#if associate
elif user_type == "associate":
    associate.associate_interface(connection)
#

#if customer
elif user_type == "customer":
    customer.customer_interface(connection)
#

else:
    print("Critical error in main.py: invalid user_type.")

connection.commit()
connection.close()
print("End of main.py")
