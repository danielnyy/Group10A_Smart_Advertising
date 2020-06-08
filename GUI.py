"""
Monash University Malaysia
FIT3162 Computer Science Project 2

Author 1: Daniel Ng Yit Yang
Author 2: Chong Jia Voon
Tested by: Justin Ang Wei-Shen

Last Edited Date: 05/06/2020

This file is the main file of the whole system. It hosts the mainview of the whole system.
More importantly when the program is started it will already run the classification of
humans with the model under the model folder. It will take a while to start because of this.

Displaying different pages inspired from Bryan Oakley
https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

Centering window inspire from
https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/

Model and display inspired from
https://github.com/dandynaufaldi/Agendernet
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from Database import *
from Page import *
from TablePage import *
from CamPage import *
from DisplayPage import *
from Classifier import *


import PIL
from PIL import Image, ImageTk
import pytesseract
import cv2
import dlib
import numpy as np
from model.mobilenetv2 import AgenderNetMobileNetV2


class MainView(tk.Frame):
    def __init__(self, db, *args, **kwargs):
        """
        The main window of the program
        """

        # initialise db
        self.db = db

        # sets the frame and the pages
        tk.Frame.__init__(self, *args, **kwargs)
        self.p1 = TablePage(db, self)
        self.p2 = CamPage(self)
        self.p3 = DisplayPage(self)

        # sets a button frame at the top, insert into the window
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        # place the button at the top
        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # set the function of each button
        b1 = tk.Button(buttonframe, text="Adverts", command=self.p1.lift)
        b2 = tk.Button(buttonframe, text="Cam", command=self.p2.lift)
        b3 = tk.Button(buttonframe, text="Display", command=self.p3.lift)

        # position the buttons
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        # show the first page first
        self.p1.show()

        # values for to be used in the few functions
        width, height = 600, 600

        # captured video object with height and width wanted
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # sets margin and image size
        self.margin = 0.4
        self.img_size = 96

        # gets the face detector
        self.detector = dlib.get_frontal_face_detector()

        # loads the model and weights
        self.model = AgenderNetMobileNetV2()
        self.model.load_weights('model/weight/mobilenetv2/mobilenet_v2-02-4.0368-0.8085-9.6728.h5')

        # calls the function to show the frame
        self.show_frame()

    def draw_label(self, image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.8, thickness=1):
        """
        This function creates the label around the face for identification
        """
        # gets the size of the label
        size = cv2.getTextSize(label, font, font_scale, thickness)[0]
        # where the position is
        x, y = point
        # gets the rectangle size
        cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
        cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)

    def show_frame(self):
        """
        This function is to run the model trained to identify human faces to be male/female and
        the age group they will be in
        """

        # sets the ad page with empty amount of people initially
        # no detection set premium ad

        if not self.db.check(self.db.select()):
            self.p3.ad = classify([])

        # reads the frame
        _, frame = self.cap.read()
        # gets image to be ready for face detection
        frame = cv2.flip(frame, 1)
        input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_h, img_w, _ = np.shape(input_img)
        # detects
        detected = self.detector(input_img, 1)
        faces = np.empty((len(detected), 96, 96, 3))
        # if detected enter here
        if len(detected) > 0:

            # for every face get their location of x and y with dimensions
            for i, d in enumerate(detected):
                x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                xw1 = max(int(x1 - self.margin * w), 0)
                yw1 = max(int(y1 - self.margin * h), 0)
                xw2 = min(int(x2 + self.margin * w), img_w - 1)
                yw2 = min(int(y2 + self.margin * h), img_h - 1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                faces[i, :, :, :] = cv2.resize(frame[yw1:yw2 + 1, xw1:xw2 + 1, :], (self.img_size, self.img_size))

            if len(faces) > 0:
                # predict ages and genders of the detected faces
                results = self.model.predict(faces)
                predicted_genders = results[0]
                ages = np.arange(0, 101).reshape(101, 1)
                predicted_ages = results[1].dot(ages).flatten()

            face_list = []
            for i, d in enumerate(detected):
                # predicts the gender
                if predicted_genders[i][0] > 0.7:
                    gend = "F"
                else:
                    gend = "M"

                # sets the label and draws it
                label = "{}, {}".format(int(predicted_ages[i]), gend)
                self.draw_label(frame, (d.left(), d.top()), label)
                # append to the list
                face_list.append([gend, int(predicted_ages[i])])

            # calculate list and give results to the ad page
            if not self.db.check(self.db.select()):
                self.p3.ad = classify(face_list)

        # show the frame and save the image shown onto the label
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.p2.label.imgtk = imgtk
        self.p2.label.configure(image=imgtk)
        # refresh after 10ms
        self.p2.label.after(10, self.show_frame)


if __name__ == "__main__":
    # create the window
    root = tk.Tk()
    root.title("Main")
    # connect to the database
    db = database()
    # connect window to the mainpage
    main = MainView(db, root)

    # set window to be in the middle
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2) - 300
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2) - 300
    root.geometry("+{}+{}".format(positionRight, positionDown))

    # set the position of the page
    main.pack(side="top", fill="both", expand=True)
    # geometry size and loop the window.
    root.wm_geometry("600x600")
    root.mainloop()


