#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 26
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

import sqlite3
import random
import engine
from engine import get_cmd

#use formatted text colors if library is available
try:
    import colorama
except Exception as error:
    print(error)
    cm = False
else:
    colorama.init()
    from colorama import Fore, Back, Style
    cm = True
#


###############################################################################

def manager_interface(conn, user):
    get_cmd("Entering Manager Mode")