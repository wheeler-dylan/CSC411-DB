#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 03 06
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

"""imports schema definition from folder and builds tables 
    in database based off their contents as column headers"""

import sys
sys.path.append("./class_definitions")
import relation

import glob #used to scan folder for files

def import_schemas(f_folder):
    """returns a list of filenames of each file in parameterized folder""" #TODO, update to build tables

    #get filenames from parameterized folder
    files = glob.glob(str(".\\" + f_folder + "\\*.csv"))
    file_names = []
    new_relations = []

    #format to remove path and extension
    for each_file in files:
        
        #file_names.append(str(each_file.replace(
        #    str(".\\" + f_folder + "\\"), "").replace(".csv", "")))
        #print(each_file)

        this_relation = relation.Relation(each_file)
        #this_relation.print_me()

        new_relations.append(this_relation)

    #

    #return list of filenames as strings
    return new_relations
#

