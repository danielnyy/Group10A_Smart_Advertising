"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is to contain the page elements to be used by the individual pages

Displaying different pages inspired from Bryan Oakley
https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

"""

import tkinter as tk


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        """
        Parent class for the pages
        """
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        """
        Shows the page
        """
        self.lift()
