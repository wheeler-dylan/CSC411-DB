"""sandbox file for testing"""

import sys
sys.path.append("./schemas")
import schemas

schemas_list = schemas.import_schemas("schemas")

print(schemas_list)

