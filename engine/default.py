#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sqlite3
import engine

def default_interface(conn, user):
    cursor = conn.cursor()
    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory").fetchall(), cursor.description) #debugging

    while(True):
        engine.print_cursor_fetch(cursor.execute( input("Enter a SQL Query:\n")).fetchall(), cursor.description)


#

