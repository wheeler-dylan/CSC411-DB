#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 03 06
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

class Relation:
    """class to aid in table building for sql queries"""

    def __init__(self, f_file): #f_file is a formatted csv file found in shcemas folder
        self.name = str(f_file.replace(str(".\\schemas\\"), "").replace(".csv", ""))
        self.file = f_file
        self.attributes = open(self.file).readline().split(",")
    #

    def print_me(self):
        print(self.name)
        print(self.attributes)
        print("\n\n\n")
    #
