"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is to hold the page to display images from the advertisements. The most important
part about this page is the use of having a button to click into a full screen to be displayed.
Also there will be a display being updated at the same time as well.

Code for refreshing images inspired from furas
https://stackoverflow.com/questions/24849265/how-do-i-create-an-automatically-updating-gui-using-tkinter

Code for full screen inspired from Brōtsyorfuzthrāx
https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter#:~:text=This%20creates%20a%20fullscreen%20window,geometry%20and%20the%20previous%20geometry.&text=You%20can%20use%20wm_attributes%20instead%20of%20attributes%20%2C%20too.

Code for image saving
http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm

Displaying different pages inspired from Bryan Oakley
https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

"""

from Page import *
import tkinter as tk
from PIL import Image, ImageTk


class DisplayPage(Page):
    def __init__(self, *args, **kwargs):
        """
        Class to display the ads into a separate screen.
        """
        Page.__init__(self, *args, **kwargs)
        self.ad = None
        tk.Button(self, text="Display", command=self.display).pack(side="top", fill="both", expand=True)

        self.label = tk.Label(self)
        self.label.pack(side="bottom", fill="both", expand=True)
        self.fs = None

    def display(self):
        """
        Called to be initially displayed
        """
        # refreshes image in main window
        self.refresh_img(self.label)
        self.full_screen()

    def refresh_img(self, lab):
        """
        This function is used to refresh the image used.
        """
        # gets the new image and stores it into image label object
        photoImageObj = tk.PhotoImage(file=self.ad)
        lab.configure(image=photoImageObj)
        lab.image = photoImageObj

        # updates the label
        self.update_idletasks()

        # after 5s check for the label only (avoid switching too abruptly)
        lab.after(5000, self.refresh_img, lab)

    def full_screen(self):
        """
        Launches a new window that shows a full screen
        """
        self.fs = tk.Toplevel()

        # binds escape to escape full screen and double click to be full screen
        self.fs.bind('<Escape>', self.small)
        self.fs.bind('<Double-Button-1>', self.large)

        # defaults full screen to be true
        self.fs.attributes("-fullscreen", True)

        # sets initial image
        photoImageObj = tk.PhotoImage(file=self.ad)
        lab = tk.Label(self.fs, image=photoImageObj)
        lab.pack()

        # refreshes image in full screen
        self.refresh_img(lab)
        self.fs.mainloop()

    def small(self, event):
        # sets to exit full screen
        self.fs.attributes("-fullscreen", False)

    def large(self, event):
        # sets to enter full screen
        self.fs.attributes("-fullscreen", True)
