
def create_product_tables(f_cursor):

    #create resistors table
    command = """CREATE TABLE resistors (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                wattage FLOAT,
                tolerance FLOAT,
                band_color_order VARCHAR(20)
                );"""
    f_cursor.execute(command) 


    #create potentiometers table
    command = """CREATE TABLE potentiometers (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                ohms FLOAT,
                turns FLOAT
                );"""
    f_cursor.execute(command)
    
    
    #create wires table
    command = """CREATE TABLE wires (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                subtype VARCHAR(30),
                price FLOAT
                );"""
    f_cursor.execute(command)


    #create soldering tools table
    command = """CREATE TABLE soldering_tools (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT
                );"""
    f_cursor.execute(command)


    #create soldering wire table
    command = """CREATE TABLE soldering_wire (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                length FLOAT
                );"""
    f_cursor.execute(command)


    #create tools table
    command = """CREATE TABLE tools (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT
                );"""
    f_cursor.execute(command)


    #create screws table
    command = """CREATE TABLE screws (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                length FLOAT
                );"""
    f_cursor.execute(command)


    #create heat shrink table
    command = """CREATE TABLE heat_shrinks (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                price FLOAT,
                size FLOAT,
                length FLOAT
                );"""
    f_cursor.execute(command)


    #create heat sink table
    command = """CREATE TABLE heat_sinks (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                price FLOAT,
                max_heat FLOAT
                );"""
    f_cursor.execute(command)


    #create electical tape table
    command = """CREATE TABLE electrical_tape (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                length FLOAT
                );"""
    f_cursor.execute(command)


    #create fans table
    command = """CREATE TABLE fans (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                size FLOAT,
                power_requirement FLOAT
                );"""
    f_cursor.execute(command)


    #create fuses table
    command = """CREATE TABLE fuses (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                amps FLOAT,
                volts FLOAT,
                blow_type VARCHAR(30)
                );"""
    f_cursor.execute(command)


    #create bulbs table
    command = """CREATE TABLE bulbs (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                color VARCHAR(20),
                wattage FLOAT
                );"""
    f_cursor.execute(command)


    #create batteries table
    command = """CREATE TABLE batteries (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                quantity INTEGER,
                voltage FLOAT
                );"""
    f_cursor.execute(command)


    #create battery charger table
    command = """CREATE TABLE battery_charger (
                object_id INTEGER PRIMARY KEY,
                model VARCHAR(30),
                brand VARCHAR(30),
                type VARCHAR(30),
                price FLOAT,
                size VARCHAR(30)
                );"""
    f_cursor.execute(command)