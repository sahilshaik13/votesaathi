import os

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "votesaathi-495109")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "chat_sessions")
RAG_CORPUS_ID = os.getenv("RAG_CORPUS_ID", "")  # Fill in after creating RAG corpus
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
