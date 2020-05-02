#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 16
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

"""establish foreign key definitions via SQL queries
   
    list of foreign keys (fk_index), includes, inorder: 
        table name, attribute to use as key, and referenced table
        all foreign keys use id as referenced attribute"""

fk_index = {"contract": [["employee_id", "employee"]],
            "orders": [["supplier_id", "supplier"],
                       ["employee_id", "employee"]],
            "inventory": [["supplier_id", "supplier"]],
            "purchases": [["customer_id", "customer"]]}


"""establish id number prefixes for various tables to ensure 
    uniqueness among various ids. Primary use is to ensure 
    itemization relations have unique table names"""

id_prefixes = {
               #"batteries": 101,
               #"battery_chargers": 102,
               #"bulbs": 103,
               #"electrical_tape": 104,
               #"fans": 105,
               #"fuses": 106,
               #"heat_shrinks": 107,
               #"heat_sinks": 108,
               #"potentiometers": 109,
               #"resistors": 110,
               #"screws": 111,
               #"soldering_tools": 112,
               #"soldering_wire": 113,
               #"tools": 114,
               #"wire": 115,
               #"contract": 201,
               #"customer": 202,
               #"employee": 203,
               #"shippers": 204,
               #"stores": 205,
               #"suppliers": 206,
               "inventory": 301,
               "orders": 302,
               "purchases": 303,
               "itemization": 401
               }