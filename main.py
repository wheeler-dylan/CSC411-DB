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

debugging_mode = False

import sqlite3 
database_filename = "BryanElectronics.db"
connection = sqlite3.connect(database_filename) 
cursor = connection.cursor() 

import product_tables

product_tables.create_product_tables(cursor)
connection.commit() 




  
# close the connection 
connection.close() 




#delete db between runs while debugging
import os
if debugging_mode:
    os.remove(database_filename)