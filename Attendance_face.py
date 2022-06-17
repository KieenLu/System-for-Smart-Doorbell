import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import mysql.connector
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv



creds = ServiceAccountCredentials.from_json_keyfile_name("attendance-faces-e054fb69a2a3.json", scope)
client = gspread.authorize(creds)

rng = "A2:A"
spreadsheetId = "1mLw0aypxbVeLJmK1-kPxFULHlQQetzH6WCrnLt6_sJk"
sheetName = "Attendance Faces"
spreadsheet = client.open_by_key(spreadsheetId)

worksheet = spreadsheet.worksheet(sheetName)

data = worksheet.get_all_records()
values = worksheet.get(rng)
max_intime = '08:00:00'


path = 'image_Attendance/'

images = []
ID_User_from_path = []
name_from_path = []
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
def run_recognition():
    video_capture = cv2.VideoCapture(0)
    count_save =0
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            ID_User_ = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                ID_User = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = name_from_path[best_match_index]
                    ID_User = ID_User_from_path[best_match_index]
                    ID_User_.append(ID_User)

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        if (len(face_names) != 0) and len(face_locations) > 0 and count_save > 100:
            count_save = 0

            nrows = len(worksheet.col_values(1))
            worksheet.update_cell(nrows + 1, 1, name)
            worksheet.update_cell(nrows + 1, 2, ID_User)
            worksheet.duplicate()

            now = datetime.now()
            date = now.strftime('%m/%d/%Y').replace('/0', '/')
            if (date[0] == '0'):
                date = date[1:]
            time = now.strftime('%H:%M:%S')
            namecell = worksheet.find(name)
            datecell = worksheet.find(date)

            if (time < max_intime):
                worksheet.update_cell(namecell.row, datecell.col, 'present')
                print('recorded')
            else:
                worksheet.update_cell(namecell.row, datecell.col, 'late')

            check_in_hour = now.strftime("%H-%M-%S")
            check_in_day = now.strftime("%Y-%m-%d")
            mycursor = db.cursor()
            mycursor.execute(
                "INSERT INTO Attendance_faces(id, FullName, Hour_check_in,Day_check_in) VALUES(%s, %s, %s, %s)",
                (ID_User, name, check_in_hour, check_in_day))
            db.commit()

            header = ['id', 'FullName', 'Hour_check_in', 'Day_check_in']
            data = [ID_User, name, check_in_hour, check_in_day]

            with open('data/data_Attendance.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)

                writer.writerow(header)

                writer.writerow(data)
        else:
            count_save += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    run_recognition()
