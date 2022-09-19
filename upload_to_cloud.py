import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import smtplib
from email.message import EmailMessage
import requests
from firebase import Firebase
import pyrebase
import datetime
import pandas as pd
from twilio.rest import Client
import keys

client = Client(keys.acc_sid, keys.auth_token)


firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
firebase = Firebase(config)


def upload_file(fileName):
    # current_time =datetime.date()
    # put image to firebase
    storage.child(fileName).put(fileName)

    auth = firebase.auth()
    email = "smartdjangosystem@gmail.com"
    password = "lutrungkien"
    user = auth.sign_in_with_email_and_password(email, password)

    url_image = storage.child(fileName).get_url(user['idToken'])

    url = f'http://13.215.178.91:4000/api/v1/devices/{device_id}/notifications'

    df = pd.read_csv('data/info_faces.csv')
    start = datetime.datetime.now()
    label = start.strftime("%Y-%m-%d_%H-%M-%S")
    for idx, data in df.iterrows():
        payload = {
            "title" : "SmartDoorbellSystem phát hiện một vị lạ trước Camera của bạn,\n Thông báo ngày : " + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"),
            "description": "Lần suất hiện của vị khác lạ mặt này vào lúc" + label,
            "imageUrl": url_image
        }
        requests.post(url, json=payload)


    message = client.messages.create(
        body="Đây là tin nhắn cảnh báo từ SmartDoorbellSystem !"
             "\nPhát hiện bất thường trước camera của bạn"
             "\nHãy kiểm tra email của bạn hoặc có thể đăng nhập vào http://13.215.178.91:4000/dashboard/notifications để xem chi tiết về sự bất thường này.",
        from_ = keys.twilio_number,
        to= keys.my_phone_number
    )
