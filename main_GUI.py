from tkinter import *
import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageTk


root = tk.Tk()
root.title("Luận Văn Tốt Nghiệp Đại Học")
root.geometry("1024x600")
root['background']='#000000'

imageCTUET= (Image.open("image_tkinter/logo_ktck.png"))
resized_imageCTUET= imageCTUET.resize((150,150))
new_imageCTUET= ImageTk.PhotoImage(resized_imageCTUET)
imageLogo1 = Label(root,image=new_imageCTUET, highlightthickness = 0, bd = 0)
imageLogo1.place(relx = 0.9, rely = 0.175, anchor = CENTER)

imageKTCK= (Image.open("image_tkinter/Logo_ctuet.png"))
resized_imageKTCK= imageKTCK.resize((150,150))
new_imageKTCK= ImageTk.PhotoImage(resized_imageKTCK)
imageLogo2 = Label(root,image=new_imageKTCK,  highlightthickness = 0, bd = 0)
imageLogo2.place(relx = 0.1, rely = 0.175, anchor = CENTER)


Label(root, text='Trường Đại học Kỹ Thuật - Công Nghệ Cần Thơ', font=("Times New Roman", 20, "bold"), bg='#000000', fg='white').place(relx = 0.5, rely = 0.075, anchor = CENTER)

Label(root, text='Khoa Kỹ Thuật Cơ Khí', font=("Times New Roman", 20, "bold"), bg='#000000', fg='white').place(relx = 0.5, rely = 0.170, anchor = CENTER)

Label(root, text='LUẬN VĂN TỐT NGHIỆP ĐẠI HỌC', font=("Times New Roman", 24, "bold"), bg='#000000', fg='white').place(relx = 0.5, rely = 0.275, anchor = CENTER)

Label(root, text='CAMERA AI: HỆ THỐNG AN NINH - KIỂM SOÁT RA VÀO TỰ ĐỘNG', font=("Times New Roman", 24, "bold"), bg='#000000', fg='white').place(relx = 0.5, rely = 0.375, anchor = CENTER)

Label(root, text='Sinh viên thực hiện : Lư Trung Kiên', font=("Times New Roman", 13), bg='#000000', fg='white').place(relx = 0.85, rely = 0.525, anchor = CENTER)
Label(root, text='Mã số sinh viên : 1800549', font=("Times New Roman", 13), bg='#000000', fg='white').place(relx = 0.85, rely = 0.575, anchor = CENTER)

Label(root, text='Cán bộ hướng dẫn :', font=("Times New Roman", 13), bg='#000000', fg='white').place(relx = 0.15, rely = 0.525, anchor = CENTER)
Label(root, text='Th.S Trần Hoài Tâm', font=("Times New Roman", 13), bg='#000000', fg='white').place(relx = 0.15, rely = 0.575, anchor = CENTER)

# imageMain= (Image.open("image_tkinter/facial-recognition.png"))
# resized_imageMain= imageMain.resize((450,250))
# new_imageMain= ImageTk.PhotoImage(resized_imageMain)
# imageLogo3 = Label(root,image=new_imageMain,  highlightthickness = 0, bd = 0)
# imageLogo3.place(relx = 0.5, rely = 0.65, anchor = CENTER)

def run_Capture():
    subprocess.run([sys.executable, "Capture_tkinter_for_Attendance_faces.py"])

def run_attendance_face():
    subprocess.run([sys.executable, "Attendance_face.py"])

def run_smartdoorbellsystem():
    subprocess.run([sys.executable, "new_v2.py", "image/", "archive/", "True"])
startButton_SDS = tk.Button(text="Lấy thông tin của bạn", width=35,command=run_Capture)
startButton_SDS.place(bordermode=tk.INSIDE, relx=0.2, rely=0.9, anchor=tk.CENTER, width=200, height=50)

startButton_Attendance_faces = tk.Button(text="Run Attendance Faces System", width=35, command=run_attendance_face)
startButton_Attendance_faces.place(bordermode=tk.INSIDE, relx=0.4, rely=0.9, anchor=tk.CENTER, width=200, height=50)

startButton_SmartDoorbell = tk.Button(text="Run SmartDoorbell System", width=35, command=run_smartdoorbellsystem)
startButton_SmartDoorbell.place(bordermode=tk.INSIDE, relx=0.6, rely=0.9, anchor=tk.CENTER, width=200, height=50)

quit_button = tk.Button( text="Quit",width=35,  command=root.destroy)
quit_button.place(bordermode=tk.INSIDE, relx=0.8, rely=0.9, anchor=tk.CENTER, width=200, height=50)

root.mainloop()
