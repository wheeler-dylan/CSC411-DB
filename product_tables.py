
def create_product_tables(f_cursor):

    #create resistors table
    command = """CREATE TABLE resistors (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                wattage FLOAT,
                tolerance FLOAT,
                band_color_order VARCHAR(20)
                );"""
    f_cursor.execute(command) 


