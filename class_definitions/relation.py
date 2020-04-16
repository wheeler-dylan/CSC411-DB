#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 03 06
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sys
sys.path.append("./class_definitions")
import foreign_keys

class Relation:
    """class to aid in table building for sql queries"""

    def __init__(self, f_file): #f_file is a formatted csv file found in shcemas folder
        self.name = str(f_file.replace(str(".\\schemas\\"), "").replace(".csv", ""))
        self.file = open(f_file)
        self.attributes = self.file.readline().rstrip('\n').split(";") #header names
        self.filetypes = self.file.readline().rstrip('\n').split(";")  #sql calls for datatypes

        #check for foreign key
        self.contains_fk = False
        if self.name in foreign_keys.fk_index.keys():
            self.contains_fk = True
    #

    def print_me(self):
        print(self.name)
        print(self.attributes)
        print(self.filetypes)
        if self.contains_fk:
            print("Foreign Keys: ", end="")
            print(foreign_keys.fk_index[self.name])
        print("\n\n\n")
    #

    def get_query(self):
        query = str("create table " + self.name + " (")
        for i in range(len(self.attributes)):            
            
            #add attribute name to query
            query = query + (str(self.attributes[i] + " " + self.filetypes[i]))

            #if first query, designate as primary key
            if i == 0:
                query = query + " primary key"
            
            #if not last query, add comma
            if i != (len(self.attributes)-1):
                query = query + ", "

        #configure foreign key if found
        if self.contains_fk:
            for each_key in foreign_keys.fk_index[self.name]:
                query = str(query + ", FOREIGN KEY (" + str(each_key[0]) +
                            ") REFERENCES " + str(each_key[1]) + "(id)" )

        query = query + ");" #end query

        return query
    #

#

