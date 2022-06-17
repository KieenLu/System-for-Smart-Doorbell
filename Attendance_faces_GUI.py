from tkinter import *
from PIL import Image, ImageTk
import cv2
import face_recognition
import os
import numpy as np
from datetime import timedelta, datetime
import pickle
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import mysql.connector


win = Tk()

# Set the size of the window
win.geometry("1024x600")

label = Label(win)
label.grid(row=0, column=0)
cap = cv2.VideoCapture(1)



creds = ServiceAccountCredentials.from_json_keyfile_name("attendance-faces-e054fb69a2a3.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Face recognition").sheet1
data = sheet.get_all_records()

max_intime = '08:00:00'

path = 'data/image'

images = []
name_from_path = []
ID_User_from_path = []
known_face_metadata = []

mylist = os.listdir(path)
for name_ in mylist:
    current_images = cv2.imread(f'{path}/{name_}')
    images.append(current_images)
    name_from_path.append(os.path.splitext(name_)[0].split('_')[0])
    ID_User_from_path.append(os.path.split(name_)[-1].split('_')[-1].split('.')[0])


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList


known_face_encodings = findEncodings(images)


def save_known_faces():
    with open("data/attendance_face.pickle", "wb") as face_data_file:
        face_data = [known_face_encodings, known_face_metadata]
        pickle.dump(face_data, face_data_file, protocol=pickle.HIGHEST_PROTOCOL)
        print("Known faces backed up to disk.")


def load_known_faces():
    global known_face_encodings, known_face_metadata

    try:
        with open("data/attendance_face.pickle", "rb") as face_data_file:
            known_face_encodings, known_face_metadata = pickle.load(face_data_file)
            print("Known faces loaded from disk.")
    except FileNotFoundError as e:
        print("No previous face data found - starting with a blank known face list.")
        pass

def show_frames():
    process_this_frame = True
    face_locations = []
    face_names = []
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)

    small_frame = cv2.resize(cv2image, (0, 0), fx=0.25, fy=0.25)

    small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)

            face_names = []
            ID_User_ = []
            if face_distances[best_match_index] < 0.65:

                # metadata = known_face_metadata[best_match_index]

                # metadata["last_seen"] = datetime.now()
                # metadata["seen_frames"] += 1
                #
                # if datetime.now() - metadata["first_seen_this_interaction"] > timedelta(minutes=1):
                #     metadata["first_seen_this_interaction"] = datetime.now()
                #     metadata["seen_count"] += 1

                name = name_from_path[best_match_index]
                face_names.append(name)

                ID_User = ID_User_from_path[best_match_index]
                ID_User_.append(name)

                # known_face_metadata.append({
                #     "first_seen": datetime.now(),
                #     "first_seen_this_interaction": datetime.now(),
                #     "last_seen": datetime.now(),
                #     "seen_count": 1,
                #     "seen_frames": 1,
                #     "face_image": images,
                #     "face_name": name,
                # })
                # print(metadata["first_seen"])

                # time_at_door = datetime.now() - metadata['first_seen_this_interaction']
                # time_notification = (time_at_door.total_seconds())
                # if 0.1 < time_notification < 1:
                #     nrows = len(sheet.col_values(1))
                #     sheet.update_cell(nrows + 1, 1, name)
                #     sheet.update_cell(nrows + 1, 2, ID_User)
                #     sheet.duplicate()
                #
                #     now = datetime.now()
                #     date = now.strftime('%m/%d/%Y').replace('/0', '/')
                #     if (date[0] == '0'):
                #         date = date[1:]
                #     time = now.strftime('%H:%M:%S')
                #     namecell = sheet.find(name)
                #     datecell = sheet.find(date)
                #
                #     if (time < max_intime):
                #         sheet.update_cell(namecell.row, datecell.col, 'present')
                #         print('recorded')
                #     else:
                #         sheet.update_cell(namecell.row, datecell.col, 'late')
                #
                #     mycursor = db.cursor()
                #     mycursor.execute(
                #         "INSERT INTO Attendance_faces(id, FullName, Check_in, Check_out, Seen_count) VALUES(%s, %s, %s, %s, %s)",
                #         (ID_User, name, metadata["first_seen_this_interaction"],
                #          metadata["last_seen"], metadata["seen_count"]))
                #     db.commit()
    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(cv2image, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(cv2image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(cv2image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    save_known_faces()

    img = Image.fromarray(cv2image)

    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(20, show_frames)

load_known_faces()
show_frames()
win.mainloop()
