from flask import Flask

from joblib import load
from sklearn.feature_extraction.text import CountVectorizer
from flask_cors import CORS
import pandas as pd
import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://mail.google.com/']
# creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# service = build('gmail', 'v1', credentials=creds)
service = None
app = Flask(__name__)
CORS(app)

predict_spam_model = load('predict_spam.joblib')
cv = CountVectorizer()
df = pd.read_csv("spam.csv", encoding="latin-1")
df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
X = df['text']
X = cv.fit_transform(X)


@app.route("/login")
def login():
    global service
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return {'message': 'success'}


@app.route("/get-normal-email")
def get_normal_email():
    result = service.users().messages().list(userId='me', labelIds='UNREAD', maxResults=10).execute().get('messages')
    message_ids = []
    for message in result:
        message_ids.append(message.get('id'))
    messages = []
    for message_id in message_ids:
        message = {}
        result = service.users().messages().get(userId='me', id=message_id).execute()
        from_email = [i['value'] for i in result.get('payload').get('headers') if i["name"] == "From"][0]
        subject = [i['value'] for i in result.get('payload').get('headers') if i["name"] == "Subject"][0]
        content = base64.b64decode(result.get('payload').get('parts')[0].get('body').get('data')).decode('utf-8')[:-2]
        if predict_spam_model.predict(cv.transform([content]))[0] == 0:
            message.update({'from_email': from_email, 'subject': subject, 'content': content})
            messages.append(message)
    return messages


@app.route("/get-spam-email")
def get_spam_email():
    result = service.users().messages().list(userId='me', labelIds='UNREAD', maxResults=10).execute().get('messages')
    message_ids = []
    for message in result:
        message_ids.append(message.get('id'))
    messages = []
    for message_id in message_ids:
        message = {}
        result = service.users().messages().get(userId='me', id=message_id).execute()
        from_email = [i['value'] for i in result.get('payload').get('headers') if i["name"] == "From"][0]
        subject = [i['value'] for i in result.get('payload').get('headers') if i["name"] == "Subject"][0]
        content = base64.b64decode(result.get('payload').get('parts')[0].get('body').get('data')).decode('utf-8')[:-2]
        if predict_spam_model.predict(cv.transform([content]))[0] == 1:
            message.update({'from_email': from_email, 'subject': subject, 'content': content})
            messages.append(message)
    return messages
