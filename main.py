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
import schemas
import foreign_keys

#filename to store db
database_filename = "BryanElectronics.db"

#delete database for recreation when in debugging mode
import os
debugging = True
if debugging:
    os.remove(database_filename)
#

#establish connection to db in order to execute sql commands
import sqlite3 
connection = sqlite3.connect(database_filename) 
cursor = connection.cursor() 


#############################################################

#build tables
tables_list = schemas.import_schemas("schemas")
print()
for each_table in tables_list.values():
    try:
        each_table.print_me()
        if debugging:
            print(each_table.get_query())
        cursor.execute(each_table.get_query())
    except sqlite3.Error as error:
        print("Error building tables from schemas folder:")
        print(error)
        if debugging:
            input("Press ENTER to continue...\n")

    print("\n")
#

#import data
for each_table in tables_list.values():
    filename = str(".\\data\\" + each_table.name + ".csv")
    this_file = open(filename, 'r')
    print(each_table.name)
    for each_line in this_file:
        cells = each_line.rstrip('\n').split(";")
        print(cells) #debugging
        
        try:
            if debugging:
                print(each_table.get_tuple_query(cells))
            cursor.execute(each_table.get_tuple_query(cells))
        except sqlite3.Error as error:
            print("Error importing tuples from data file " + filename + ":")
            print("tuple data: " + str(each_line)) 
            print(error)
            if debugging:
                input("Press ENTER to continue...\n")
    #
    print("")

print("End of main.py")
