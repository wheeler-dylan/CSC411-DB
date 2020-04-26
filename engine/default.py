#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sqlite3
import engine

#use formatted text colors if library is available
try:
    import colorama
except:
    print("Colorama library not found.")
    color_mode = False
else:
    print("Color formatting activated.") #debugging
    color_mode = True
#


def default_interface(conn, user):
    cursor = conn.cursor()

    engine.print_cursor_fetch(cursor.execute("SELECT * FROM inventory").fetchall(), cursor.description) #debugging
    print()

    command = ""
    command_list = str("select an option from the commands below:\n" +
                       "\t(commands are case sensitive)\n" +
                       "exit: exit the program\n" +
                       "help: display commands list\n" +
                       "orders: view all orders made and amounts sold\n" +
                       "bestsellers: view best selling items by location\n" +
                       "employ: hire or fire a manager or associate\n" +
                       "pay: issue paychecks\n" +
                       "losses: check for lost or broken items\n" +
                       "suppliers: alter suppliers and shippers\n" +
                       "SQL: enter SQL query mode\n") 
    print(command_list)


    while(command != "exit"):

        command = input()
        
        if command == "exit":
            continue

        elif command == "help":
            print(command_list)
            continue

        #SQL MODE
        elif command == "SQL":
            print("Now entering SQL mode, all other commands are now invalid.\n" + 
                  "enter 'exit' to leave SQL mode.\n")

            query = ""
            while query != "exit":
                query = input("Enter a SQL Query:\n")

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

        #End SQL mode

        else:
            print("Invalid command entered.")
            print(command_list)

        #end command switch block

    #end while command != exit

#end default_interface()

