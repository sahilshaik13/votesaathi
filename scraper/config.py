"""
Scraper service configuration — minimal, no Secret Manager dependency.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "votesaathi-495109")
GCP_PROJECT_NUMBER = os.getenv("GCP_PROJECT_NUMBER", "171624099766")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "votesaathi-bcf9e")
FIREBASE_DATABASE_URL = os.getenv(
    "FIREBASE_DATABASE_URL",
    f"https://{FIREBASE_PROJECT_ID}-default-rtdb.firebaseio.com"
)
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "chat_sessions")
