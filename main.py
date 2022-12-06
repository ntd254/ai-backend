from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from base64 import urlsafe_b64decode

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def base64_url_decode(base64_url):
    padding = b'=' * (4 - (len(str(base64_url)) % 4))

    return urlsafe_b64decode(base64_url + padding)


def get_message():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me', maxResults=10).execute()
    # message = service.users().messages().get(userId='me', id='184e7ac88fe4c8b4').execute()
    # content = base64.b64decode(message.get('payload').get('parts')[0].get('body').get('data')).decode('utf-8')[:-2]
    # message1 = service.users().messages().get(userId='me', id='184c3bc47e62dcd2').execute()
    # text = message1.get('payload').get('parts')[0].get('body').get('data')
    # print(str(urlsafe_b64decode(text), 'utf-8'))
    message2 = service.users().messages().get(userId='me', id='184e7f114cb09c68').execute()
    print(message2.get('payload').get('mimeType') == 'multipart/mixed')


if __name__ == '__main__':
    # main()
    get_message()
