import base64
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials and os.path.exists(firebase_credentials):
    cred = credentials.Certificate(firebase_credentials)
else:
    firebase_credentials_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
    if not firebase_credentials_base64:
        raise ValueError("No Firebase credentials found!")

    decoded_credentials = json.loads(base64.b64decode(firebase_credentials_base64).decode("utf-8"))
    cred = credentials.Certificate(decoded_credentials)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
