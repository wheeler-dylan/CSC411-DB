"""sandbox file for testing"""

print("------------------------------- running sandbox.py -------------------------------")

import sys
sys.path.append("./schemas")
import schemas

schemas_list = schemas.import_schemas("schemas")

for each_table in schemas_list:
    each_table.print_me()
#

