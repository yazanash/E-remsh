import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
import firebase_admin
from firebase_admin import credentials,messaging

# Initialize Firebase
FIREBASE_CREDENTIALS = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
}
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)



def send_push_notification(token, title, body):
    # Create a message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,  # The recipient's device token
    )

    # Send the message
    response = messaging.send(message)
    print('Successfully sent message:', response)