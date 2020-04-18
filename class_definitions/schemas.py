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
    """returns a list of relations built from each file in parameterized folder"""
    new_relations = {}

    #get filenames from parameterized folder
    files = glob.glob(str(".\\" + f_folder + "\\*.csv"))

    #build new relation from each file
    for each_file in files:
        filename = str(each_file.replace(str(".\\schemas\\"), "").replace(".csv", ""))
        print("Converting " + str(filename) + ".csv to relation...")
        this_relation = relation.Relation(each_file)
        new_relations[filename] = this_relation
    #
    print()

    #return list of filenames as strings
    return new_relations
#

