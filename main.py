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
import schemas
schemas_list = schemas.import_schemas("schemas")

#filename to store db
database_filename = "BryanElectronics.db"

#delete database for recreation when in debugging mode
import os
debugging_mode = False
if debugging_mode:
    os.remove(database_filename)
#

#establish connection to db in order to execute sql commands
import sqlite3 
connection = sqlite3.connect(database_filename) 
cursor = connection.cursor() 


#############################################################

for each_table in schemas_list:
    each_table.print_me()
    cursor.execute(each_table.get_query())
#

#contract = schemas_list[0]
#print(contract.get_query())




#delete db between runs while debugging
if debugging_mode:
    os.remove(database_filename)