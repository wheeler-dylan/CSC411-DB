print("------------------------- running sandbox.py -------------------------")

import glob

def import_schemas(f_folder):
    """returns a list of filenames of each file in parameterized folder""" 
    #get filenames from parameterized folder
    files = glob.glob(str(".\\" + f_folder + "\\*.csv"))
    file_names = []

    #format to remove path and extension
    for each_file in files:
        file_names.append(str(each_file.replace(
            str(".\\" + f_folder + "\\"), "").replace(".csv", "")))
        #print(each_file)
    #

    #return list of filenames as strings
    return file_names
#

