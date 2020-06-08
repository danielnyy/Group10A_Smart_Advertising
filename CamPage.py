"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is to host the page to display the camera output. It's label will be called in the
GUI.py file.

Displaying different pages inspired from Bryan Oakley
https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

"""

from Page import *
import tkinter as tk


class CamPage(Page):
    def __init__(self, *args, **kwargs):
        """
        A page to show a label which is the camera only.
        """
        Page.__init__(self, *args, **kwargs)
        self.label = tk.Label(self)
        self.label.pack()
