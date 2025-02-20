import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

firebase_key_path = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_key_path:
    raise ValueError("FIREBASE_CREDENTIALS not found. Set it in .env file.")

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
