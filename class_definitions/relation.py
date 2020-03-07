#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 03 06
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

class Relation:
    """class to aid in table building for sql queries"""

    def __init__(self, f_file): #f_file is a formatted csv file found in shcemas folder
        self.name = str(f_file.replace(str(".\\schemas\\"), "").replace(".csv", ""))
        self.file = open(f_file)
        self.attributes = self.file.readline().split(";") #header names
        self.filetypes = self.file.readline().split(";")  #sql calls for datatypes
    #

    def print_me(self):
        print(self.name)
        print(self.attributes)
        print(self.filetypes)
        print("\n\n\n")
    #

    def get_query(self):
        query = str("create table " + self.name + " (")
        for i in range(len(self.attributes)):
            query = query + (str(self.attributes[i] + " " + self.filetypes[i]))
            if i == 0:
                query = query + " primary key"
            if i != (len(self.attributes)-1):
                query = query + ", "
        query = query + ");"

        return query
    #

#

