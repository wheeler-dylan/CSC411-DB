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
