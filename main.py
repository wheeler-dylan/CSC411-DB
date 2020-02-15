#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 02 15
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

#uses tutorial found at https://www.geeksforgeeks.org/sql-using-python/

import sqlite3 
connection = sqlite3.connect("BryanElectronics.db") 

"""
SQLite3 uses the following cycle to execute SQL commands:
    connection = sqlite3.connect("BryanElectronics.db")     //establishes DB file
    crsr = connection.cursor()  //build cursor to SQL interpretter, commands entered at this point
    sql_command = "string"      //write a SQL command and store as a string
    crsr.execute(sql_command)   //execute the SQL command
    connection.commit()         //saves changes to the database
    connection.close()          //closes connection
"""

# cursor  
crsr = connection.cursor() 
  
# SQL command to create a table in the database 
sql_command = str("CREATE TABLE resistors ( " +
                  "object_id INTEGER PRIMARY KEY, " +
                  "model VARCHAR(30), " +
                  "wattage INTEGER, " +
                  "" +
                  ");")

  
# execute the statement 
crsr.execute(sql_command) 
  
# SQL command to insert the data in the table 
sql_command = """INSERT INTO emp VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");"""
crsr.execute(sql_command) 
  
# another SQL command to insert the data in the table 
sql_command = """INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");"""
crsr.execute(sql_command) 
  
# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
connection.commit() 
  
# close the connection 
connection.close() 


