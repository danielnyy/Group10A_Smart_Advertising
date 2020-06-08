"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is a file meant to create and have function to deal with the database. It will be very
closely linked to TablePage.py and have its error handled whenever any functions will be
called from this.

Code for most of this inspired from
https://www.tutorialspoint.com/sqlite/sqlite_python.htm

Code for row checking inspired from SamerAlshurafa
https://forums.xamarin.com/discussion/60818/sqlitedatabase-how-to-check-if-record-or-row-is-exist-in-table

Code for table checking inspired from PoorLuzer
https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists

"""

import sqlite3
import os


class database:
    def __init__(self):
        """
        Creates db class
        """
        # creates the class
        self.db = None
        self.connect()
        self.create()

    def check(self, cursor):
        """
        This is to check if the cursor exist
        """
        # checks if anything exist
        count = 0
        for c in cursor:
            count += 1
        self.db.close()
        if count == 0:
            return True
        else:
            return False

    def table_check(self):
        """
        checks if the table exist before creating it
        """
        self.connect()
        cursor = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MST_AD';")
        return self.check(cursor)

    def row_check(self, id):
        """
        checks if the id exist first
        """
        self.connect()
        cursor = self.db.execute("SELECT * FROM MST_AD WHERE COMP_ID=" + str(id) + ";")
        return self.check(cursor)

    def connect(self):
        """
        connects to the db file
        """
        # creates new one if old is not found
        self.db = sqlite3.connect('ad.db')

    def create(self):
        """
        creates the table
        """
        if self.table_check():
            self.connect()
            self.db.execute('''CREATE TABLE MST_AD
                        (COMP_ID                   INT PRIMARY KEY NOT NULL,
                        COMP_NAME                  TEXT NOT NULL,
                        PATH_NAME                  TEXT NOT NULL,
                        AGE                        TEXT NOT NULL,
                        GENDER                     CHAR(1),
                        PREMIUM                    CHAR(1),
                        DEL                        CHAR(1));
                        ''')
            self.db.close()
            return True
        self.db.close()
        return False

    def add(self, id, name, path_name, age, gender, prm):
        """
        add rows into the table based on inserted values
        """
        if self.row_check(id):
            self.connect()
            self.db.execute("INSERT INTO MST_AD (COMP_ID,COMP_NAME,PATH_NAME,AGE,GENDER,PREMIUM,DEL) \
                  VALUES ("+str(id)+", '"+name+"', '"+path_name+"', '"+age+"', '"+gender+"', '"+prm+"', 'N' )")

            # have to commit for it to work
            self.db.commit()
            self.db.close()
            return True
        self.db.close()
        return False

    def edit(self, edit_id, path_name, age, gender, prm):
        """
        Edits row based on what is given
        """
        if self.row_check(edit_id) is False:
            self.connect()
            self.db.execute("UPDATE MST_AD SET PATH_NAME='" + path_name +"',"
                            "AGE='" + age +"', GENDER='" + gender +"', PREMIUM='" + prm +"' WHERE COMP_ID = " + str(edit_id))
            self.db.commit()
            self.db.close()
            return True
        self.db.close()
        return False

    def delete(self, id):
        """
        soft delete rows by updating a variable, can be retrievable
        """
        if self.row_check(id) is False:
            self.connect()
            self.db.execute("UPDATE MST_AD SET DEL='Y' WHERE COMP_ID = "+str(id)+";")
            self.db.commit()
            self.db.close()
            return True
        self.db.close()
        return False

    def select(self):
        """
        Selectes non soft deleted rows
        """
        # select not deleted rows
        self.connect()
        cursor = self.db.execute("SELECT * FROM MST_AD WHERE DEL = 'N'")
        return cursor

    def get_db(self):
        """
        gets the db to close
        """
        return self.db

    def runsql(self, sql):
        """
        This function is to run sql commands by the back end user in case of anything
        """
        self.connect()
        cursor = self.db.execute(sql)
        self.db.commit()
        return cursor

