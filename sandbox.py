"""sandbox file for testing"""

print("------------------------------- running sandbox.py -------------------------------")

import sys
sys.path.append("./schemas")
import schemas
schemas_list = schemas.import_schemas("schemas")

#filename to store db
database_filename = "BryanElectronics.db"

#delete database for recreation when in debugging mode
import os
debugging_mode = True
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