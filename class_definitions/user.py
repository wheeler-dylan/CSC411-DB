#Author:        Dylan E. Wheeler
#Email:         dylan.wheeler@usm.edu
#Date:          2019 04 25
#Course:        CSC411 - Intro to Databases
#Prof.:         Dr. Bo Li

class User():
    def __init__(self, f_type, f_id, f_permissions, f_username, f_password):
        self.type = f_type  #str, name of table to be added to
        self.id = f_id      #int, used as primary key on that table
        self.permissions = f_permissions
        self.username = f_username
        self.password = f_password
    #

    def configure_employee(self):
        pass

    def configure_customer(self):
        pass

    def add_to_table(self):
        pass
#

default_users = {}
default_users["DEFAULT_DBAdmin"] = User("employee", 4434430001, "admin", "DEFAULT_DBAdmin", "8Q@3^r`{;@AV#g_z")

