#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 16
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

"""establish foreign key definitions via SQL queries
    cite: https://stackoverflow.com/questions/10028214/add-foreign-key-to-existing-table
    example: ALTER TABLE t_name1 ADD FOREIGN KEY (column_name) REFERENCES t_name2(column_name)
    must be ran after tables are built via schemas.py"""

"""list of foreign keys, includes, inorder: 
   table name, attribute to use as key, and referenced table
   all foreign keys use id as referenced attribute"""
fk_index = {"contract": ["employee_id", "employee"] }
