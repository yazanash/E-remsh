# import os
# from dotenv import load_dotenv
#
# # Load the .env file
# load_dotenv()
# import firebase_admin
# from firebase_admin import credentials,messaging
#
# # Initialize Firebase
# FIREBASE_CREDENTIALS = {
#     "type": os.getenv("FIREBASE_TYPE"),
#     "project_id": os.getenv("FIREBASE_PROJECT_ID"),
#     "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
#     "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
# }
# cred = credentials.Certificate(FIREBASE_CREDENTIALS)
# firebase_admin.initialize_app(cred)
#
#
#
# def send_push_notification(token, title, body):
#     # Create a message
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         token=token,  # The recipient's device token
#     )
#
#     # Send the message
#     response = messaging.send(message)
#     print('Successfully sent message:', response)


import json
import requests
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

print(os.getenv("project_id"))
def create_credentials_from_env():

    private_key = os.getenv("private_key").replace("\\n", "\n")
    service_account_info = {
        "type": os.getenv("type"),
        "project_id":  os.getenv("project_id"),
        "private_key_id": os.getenv("private_key_id"),
        "private_key": private_key,
        "client_email": os.getenv("client_email"),
        "client_id": os.getenv("client_id"),
        "auth_uri": os.getenv("auth_uri"),
        "token_uri": os.getenv("token_uri"),
        "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
        "client_x509_cert_url": os.getenv("client_x509_cert_url"),
    }
    credentials = Credentials.from_service_account_info(service_account_info,scopes=["https://www.googleapis.com/auth/cloud-platform"])
    return credentials


def send_fcm_v1_notification(token, title, body):
    # Load the service account key
    credentials = create_credentials_from_env()
    credentials.refresh(Request())
    access_token = credentials.token
    # print(access_token)
    # Generate an access token
    # access_token = credentials.token

    # Prepare the HTTP request
    url = "https://fcm.googleapis.com/v1/projects/eremsh/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            },
        }
    }

    # Make the HTTP request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print( response.json())
