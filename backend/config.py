"""
VoteSaathi configuration — loads environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "votesaathi-495109")
GCP_PROJECT_NUMBER = os.getenv("GCP_PROJECT_NUMBER", "171624099766")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "chat_sessions")
RAG_CORPUS_ID = os.getenv("RAG_CORPUS_ID", "")  # Fill in after creating RAG corpus
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FIREBASE_APPLICATION_CREDENTIALS = os.getenv("FIREBASE_APPLICATION_CREDENTIALS")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "votesaathi-495109")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", f"https://{FIREBASE_PROJECT_ID}-default-rtdb.firebaseio.com")

# Fetch sensitive secrets dynamically from GCP Secret Manager
try:
    from services.secret_manager import get_secret
    JWT_SECRET_KEY = get_secret("VOTESAATHI_JWT_SECRET")
except Exception as e:
    print(f"Warning: Failed to load JWT_SECRET_KEY from Secret Manager: {e}")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-for-dev")

JWT_ALGORITHM = "HS256"
