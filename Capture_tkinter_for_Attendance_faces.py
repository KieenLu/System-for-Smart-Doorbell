import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
import pyrebase
import os
config = {

  "apiKey": "AIzaSyCbVXkvGT8OCeGTnogXENUyge2fq86ngTs",
  "authDomain": "attendance-faces-824a8.firebaseapp.com",
  "projectId": "attendance-faces-824a8",
    "databaseURL": "https://smartdoorbellsystem-19df7-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "attendance-faces-824a8.appspot.com",
  "messagingSenderId": "845411246113",
  "appId": "1:845411246113:web:f28896bcbbdd3fde818360",

}
firebase  = pyrebase.initialize_app(config)
storage = firebase.storage()


cancel = False



def prompt_ok(event=0):
    global cancel, buttonCapture, button1, button2
    cancel = True

    buttonCapture.place_forget()
    button1 = tk.Button(mainWindow, text="Good Image!", command=saveAndExit)
    button2 = tk.Button(mainWindow, text="Try Again", command=resume)
    button1.place(anchor=tk.CENTER, relx=0.6, rely=0.9, width=150, height=50)
    button2.place(anchor=tk.CENTER, relx=0.85, rely=0.9, width=150, height=50)
    button1.focus()


def resume(event=0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    buttonCapture.place(bordermode=tk.INSIDE, relx=0.8, rely=0.9, anchor=tk.CENTER, width=200, height=50)
    lmain.after(10, show_frame)



cap = cv2.VideoCapture(0)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()

mainWindow = tk.Tk()
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.LEFT, anchor=tk.CENTER, relief=tk.RAISED)
buttonCapture = tk.Button(mainWindow, text="Capture", command=prompt_ok)


labelName = tk.Label(mainWindow, text="Nhập tên của bạn : ")
labelName.place(bordermode=tk.INSIDE, relx=0.125, rely=0.2, anchor=tk.CENTER, width=150, height=25)

textName = tk.Entry(mainWindow)
textName.insert(0, "VD : TranVanA")
textName.place(bordermode=tk.INSIDE, relx=0.4, rely=0.85, anchor=tk.CENTER, width=100, height=25)


labelID = tk.Label(mainWindow, text="Nhập ID/MSSV của bạn : ")
labelID.place(bordermode=tk.INSIDE, relx=0.125, rely=0.95, anchor=tk.CENTER, width=150, height=25)

textID = tk.Entry(mainWindow)
textID.insert(0, "VD : 123456")
textID.place(bordermode=tk.INSIDE, relx=0.4, rely=0.95, anchor=tk.CENTER, width=100, height=25)



lmain.pack()
buttonCapture.place(bordermode=tk.INSIDE, relx=0.8, rely=0.9, anchor=tk.CENTER, width=200, height=50)
buttonCapture.focus()

def saveAndExit(event=0):
    global prevImg
    name = (textName.get())
    ID = (textID.get())
    path_cloud = "image_from_Attendance_faces_system/"+name + "_" + ID + ".png"
    if (len(sys.argv) < 2):
        filepath = "image_Attendance/"+name + "_" + ID + ".png"
    else:
        filepath = sys.argv[1]

    print("Output file to: " + filepath)
    prevImg.save(filepath)
    storage.child(path_cloud).put(filepath)

def show_frame():
    global cancel, prevImg, buttonCapture

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)


show_frame()
mainWindow.mainloop()