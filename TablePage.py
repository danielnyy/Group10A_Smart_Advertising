"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is to host the interaction with the database for the user. It has many GUI aspects and
can be quite fragile but would not cause the app to crash.

Displaying different pages inspired from Bryan Oakley
https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

Displaying table inspired from j_4321
https://stackoverflow.com/questions/50625306/what-is-the-best-way-to-show-data-in-a-table-in-tkinter/50651988#50651988

Centering window inspire from
https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/

Toplevel inspired from
https://www.tutorialspoint.com/python/tk_toplevel.htm#:~:text=Toplevel%20widgets%20work%20as%20windows,number%20of%20top%2Dlevel%20windows.
"""

import tkinter as tk
from PIL import Image
from tkinter import ttk
from tkinter import filedialog
from Database import *
from Page import *


class TablePage(Page):
    def __init__(self, db, *args, **kwargs):
        """
        This class is for the page to interact with the database
        """
        # creates the page
        Page.__init__(self, *args, **kwargs)

        # creates tree, makes the table, initialise the database and inserts latest
        # database values
        self.tree = None
        self.table()
        self.db = db
        self.refresh()

        self.id = tk.IntVar()
        self.name = tk.StringVar()
        self.file = ""
        self.age = tk.StringVar()
        self.gender = tk.StringVar()
        self.prm = tk.StringVar()
        self.item = None

    def picture_check(self):
        """
        This function is to check if the value of the file is a jpg, if its a jpg,
        it can't be seen within tkinter. Therefore, we have to create a png version of it
        and add it into the folder.
        """
        if self.file[-3] == 'j':
            # saves a png file and sets that as the new filename path
            im1 = Image.open(self.file)
            self.file = self.file[0:-3] + 'png'
            im1.save(self.file)

    def select_item(self, a):
        """
        This function is to get the item that is highlighted and selected to be edited or delete
        """
        # focuses on the item
        # returns the id of the item
        cur_item = self.tree.focus()
        # sets item based on the id
        self.item = self.tree.item(cur_item)

    def filepath(self):
        """
        Obtain the filepath based on the function and then checks if its a jpg or png
        """
        self.file = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"),
                                                                                   ("png files", "*.png")))
        self.picture_check()

    def refresh(self):
        """
        This function is to obtain values from the database so it can refresh the table
        """
        # deletes all the values in the table
        self.tree.delete(*self.tree.get_children())

        # selects from the database
        cursor = self.db.select()
        for c in cursor:
            # insert values into the table
            self.tree.insert("", "end", values=(c[0], c[1], c[2], c[3], c[4], c[5]))
        return True

    def table(self):
        """
        Creates the main page of table page
        """
        # Sets the title of the name
        top = tk.Label(self, text="Advertisements", font=("Arial", 30)).grid(row=0, columnspan=4)
        # Title of the tables
        cols = (['ID', 50], ['Name', 100], ['File Path', 250], ['Age', 60], ['Gender', 60], ['Premium', 60])
        # initialise the tree
        self.tree = ttk.Treeview(self, columns=cols, show='headings')

        # sets the scrollbar
        vbar = tk.Scrollbar(top, orient="vertical", command=self.tree.yview)
        vbar.pack(side='right', fill='y')
        self.tree.configure(yscroll=vbar.set)

        # sets the headers for the table
        for i in range(len(cols)):
            self.tree.column(i, width=cols[i][1], anchor="center")
            self.tree.heading(i, text=cols[i][0])

        # binds selected item
        self.tree.bind('<ButtonRelease-1>', self.select_item)
        # sets tree at top of window
        self.tree.grid(row=1, column=0, columnspan=4)

        # sets all button
        sqlButton = tk.Button(self, text="SQL", width=15, command=self.sql).grid(row=4, column=0)
        addButton = tk.Button(self, text="Add", width=15, command=self.add).grid(row=4, column=1)
        editButton = tk.Button(self, text="Edit", width=15, command=self.edit).grid(row=4, column=2)
        delButton = tk.Button(self, text="Delete", width=15, command=self.delete).grid(row=4, column=3)

    def sql(self):
        """
        Function called when button is clicked, the purpose is to run sql commands
        within the gui itself
        """
        # opens a new window to fill details
        sql_view = tk.Toplevel()
        sql_string = tk.StringVar(value="UPDATE MST_AD SET DEL='N' WHERE COMP_ID=")

        # button saved will cause this inner function
        def func_sql():
            """
            add sql commands into the database
            """
            try:
                # runs it in the db
                self.db.runsql(sql_string.get())
                self.pop('Saved!')

            # catches error and not saved
            except:
                self.pop('Error!')

            # destroys window and refresh values
            sql_view.destroy()
            self.refresh()

        # sets the textbox to insert the command
        et = tk.Entry(sql_view, width=100, textvariable=sql_string)
        et.pack(side="top", fill="both", expand=True)

        # sets the button to click when done writing command
        button = tk.Button(sql_view, text='run',command=func_sql)
        button.pack(side="bottom", fill="both", expand=True)

        # sets title and makes sure the window is launch in the middle of the screen
        sql_view.title('SQL Command')
        self.position(sql_view)

    def repeat(self, view):
        """
        Function that creates the same values for edit and add. Set there to reduce redundancy
        """
        # labels
        label_id = tk.Label(view, text="Company ID:", font=("Arial", 12)).grid(row=0, column=1)
        label_name = tk.Label(view, text="Company Name:", font=("Arial", 12)).grid(row=1, column=1)
        label_file = tk.Label(view, text="File Path:", font=("Arial", 12)).grid(row=2, column=1)
        label_age = tk.Label(view, text="Age:", font=("Arial", 12)).grid(row=3, column=1)
        label_gender = tk.Label(view, text="Gender:", font=("Arial", 12)).grid(row=4, column=1)
        label_prm = tk.Label(view, text="Premium:", font=("Arial", 12)).grid(row=5, column=1)

        # Edit boxes
        btn_file = tk.Button(view, text='File',command=self.filepath).grid(row=2, column=2)
        cmb_age = ttk.Combobox(view,
                               values=["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80",
                                        "80-90", "90-100"], textvariable=self.age).grid(row=3, column=2)

        # radio buttons
        rdn_gdr_male = tk.Radiobutton(view, text='Male', value='M', variable=self.gender)
        rdn_gdr_male.grid(row=4, column=3)
        rdn_gdr_female = tk.Radiobutton(view, text='Female', value='F', variable=self.gender)
        rdn_gdr_female.grid(row=4, column=2)
        rdn_prm_no = tk.Radiobutton(view, text='No', value='N', variable=self.prm)
        rdn_prm_no.grid(row=5, column=3)
        rdn_prm_yes = tk.Radiobutton(view, text='Yes', value='Y', variable=self.prm)
        rdn_prm_yes.grid(row=5, column=2)

    def add(self):
        """
        Goes to this window when button is clicked, to add values into the database
        """

        # creates window with repeated function
        add_view = tk.Toplevel()
        self.repeat(add_view)

        def insert():
            """
            add rows into the database
            """
            try:
                # checks if its possible to add
                if self.db.add(self.id.get(), self.name.get(), self.file, self.age.get(), self.gender.get(),
                               self.prm.get()):
                    # successfully added
                    lbl = 'Saved!'
                    add_view.destroy()
                else:
                    # can't be added
                    lbl = 'ID already exist try again'

            except:
                # catches error when labels are not inserted properly
                lbl = 'Error! Labels not saved properly.'

            # calls the label in pop
            self.pop(lbl)
            # refreshes data in table
            self.refresh()

        # Sets the id and name as text
        txt_id = tk.Entry(add_view, width=10, textvariable=self.id).grid(row=0, column=2)
        txt_name = tk.Entry(add_view, width=20, textvariable=self.name).grid(row=1, column=2)
        # save button
        btn_save = tk.Button(add_view, text='Save', command=insert).grid(row=6, column=2)

        # adds title and the window to be in the middle
        add_view.title('Add')
        self.position(add_view)

    def edit(self):
        """
        Once edit button is clicked, this function is called and it is to edit the selected item
        """
        try:
            # checks if self.item is selected
            item = self.item['values']
            # rests to empty so they have to select it again
            self.item = None

            # creates the window with repeat function
            edit_view = tk.Toplevel()
            self.repeat(edit_view)

            def insert():
                """
                edits value into the database based on the ID
                """
                # gets the new values
                file = self.file
                age = self.age.get()
                gen = self.gender.get()
                prm = self.prm.get()

                # if emtpy use previous value
                if file == "":
                    file = item[2]
                if age == "":
                    age = item[3]
                if gen == "":
                    gen = item[4]
                if prm == "":
                    prm = item[5]

                # save values
                if self.db.edit(item[0], file, age, gen, prm):
                    lbl = 'Saved!'
                    edit_view.destroy()

                # doesn't save
                else:
                    lbl = 'ID does not exist, try again.'
                self.pop(lbl)
                self.refresh()

            # labels for id and name as they should never be changed as primary keys
            label_edit_id = tk.Label(edit_view, text=item[0], font=("Arial", 12)).grid(row=0, column=2)
            label_edit_name = tk.Label(edit_view, text=item[1], font=("Arial", 12)).grid(row=1, column=2)
            # button
            btn_save = tk.Button(edit_view, text='Save', command=insert).grid(row=6, column=2)

            # title and set window in middle
            edit_view.title('Edit')
            self.position(edit_view)

        # catches when the row is not selected
        except TypeError or IndexError:
            self.pop('Error! No Row Selected.')

    def delete(self):
        """
        delete function called when clicked on, soft delete function
        """
        try:
            # gets the item
            del_item = self.item['values']
            # resets to None
            self.item = None

            # gets the id
            del_id = del_item[0]

            # create new window
            txt = 'Are you sure you want to DELETE ' + str(del_id) + ', ' + str(del_item[1]) + '?'
            del_view = tk.Tk()

            def delete_view():
                """
                function to delete view
                """
                del_view.destroy()

            def dlt():
                """
                function called when it is confirmed to be deleted
                """
                # Deletes
                if self.db.delete(del_id):
                    lbl = 'Deleted!'
                else:
                    lbl = "Can't Delete!"
                self.pop(lbl)
                delete_view()
                self.refresh()

            # Label and button to check if the user wants to delete
            tk.Label(del_view, text=txt, font=("Arial", 12))\
                .pack(side="top", fill="both", expand=True)
            tk.Button(del_view, text='Yes',command=dlt)\
                .pack(side="left", fill="both", expand=True)
            tk.Button(del_view, text='No',command=delete_view)\
                .pack(side="right", fill="both", expand=True)

            # sets title and window to be middle
            del_view.title('Delete')
            self.position(del_view)

        # catches error where row item is not selected
        except TypeError or IndexError:
            self.pop('Error! Row not selected.')

    def pop(self, lbl):
        """
        A popup window to present a certain information
        """
        popup = tk.Toplevel()

        def close():
            popup.withdraw()

        # label to show information
        label = tk.Label(popup, text=lbl, font=("Arial", 12))
        label.pack(side="top", fill="both", expand=True)

        # button to click okay to close
        button = tk.Button(popup, text='Ok',command=close)
        button.pack(side="bottom", fill="both", expand=True)

        # set title and sets window to be in the middle
        popup.title('Message')
        self.position(popup)

    @staticmethod
    def position(viewer):
        """
        Code to set tkinter to be in the middle of the page
        """
        # gets the max size height and width
        windowWidth = viewer.winfo_reqwidth()
        windowHeight = viewer.winfo_reqheight()

        # sets position x and y
        positionRight = int(viewer.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(viewer.winfo_screenheight() / 2 - windowHeight / 2)

        # sets where it appears
        viewer.geometry("+{}+{}".format(positionRight, positionDown))