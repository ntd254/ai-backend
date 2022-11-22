from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64

SCOPES = ['https://mail.google.com/']

creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('gmail', 'v1', credentials=creds)
# result = service.users().messages().list(userId='me', labelIds='UNREAD', maxResults=10).execute()
# messages = result.get('messages')
# print(messages)
# text = service.users().messages().get(userId='me', id='1841e192670f79a3').execute()
# # print(text.get('payload').get('headers'))
# headers = text.get('payload').get('headers')
# for header in text.get('payload').get('headers'):
#     print(header)
# data = text.get('payload').get('parts')[0].get('body').get('data')
# # data = data.replace("-", "+").replace("_", "/")
# content = base64.b64decode(data).decode('utf-8')
# print(base64.b64decode(data).decode('utf-8'))
# subject = [i['value'] for i in headers if i["name"] == "Subject"][0]
# from_email = [i['value'] for i in headers if i["name"] == "From"][0]
# print(from_email)
# print(subject)
# json = {}
# json.update({'from': from_email, 'subject': subject, 'content': content})
# print(json)

# for key, value in text.get('payload').items():
#     print(key, value)
result = service.users().messages().list(userId='me', labelIds='UNREAD', maxResults=1).execute().get('messages')
message_ids = []
for message in result:
    print(message)
    message_ids.append(message.get('id'))

messages = []
for message_id in message_ids:
    message = {}
    result = service.users().messages().get(userId='me', id=message_id).execute()
    from_email = [i['value'] for i in result.get('payload').get('headers') if i["name"] == "From"][0]
    subject = [i['value'] for i in result.get('payload').get('headers') if i["name"] == "Subject"][0]
    content = base64.b64decode(result.get('payload').get('parts')[0].get('body').get('data')).decode('utf-8')[:-2]
    message.update({'from_email': from_email, 'subject': subject, 'content': content})
    messages.append(message)

print(messages)


