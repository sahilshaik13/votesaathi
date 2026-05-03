import firebase_admin
from firebase_admin import credentials, db
from config import FIREBASE_DATABASE_URL, FIREBASE_APPLICATION_CREDENTIALS
import logging

logger = logging.getLogger(__name__)

import os
# Initialize Firebase Admin once
# Initialize Firebase Admin once with extreme safety
try:
    if not firebase_admin._apps:
        # Check potential credential paths
        paths_to_check = [
            FIREBASE_APPLICATION_CREDENTIALS,
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            "service-account.json",
            "votesaathi-bcf9e-firebase-adminsdk-fbsvc-c3e2b36673.json"
        ]
        
        cred_path = None
        for p in paths_to_check:
            if p and os.path.exists(p):
                cred_path = p
                break
        
        if cred_path:
            logger.info(f"Initializing Firebase with credentials from {cred_path}")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})
        else:
            logger.info("Initializing Firebase with default Application Default Credentials")
            firebase_admin.initialize_app(options={'databaseURL': FIREBASE_DATABASE_URL})
            
except Exception as e:
    logger.error(f"Non-blocking Firebase initialization error: {e}")

def update_realtime_news(news_list, query=None):
    """
    Pushes news updates to Firebase Realtime Database.
    If query is provided, updates a specific node.
    """
    try:
        path = f"live/news/{query}" if query else "live/news/general"
        ref = db.reference(path)
        ref.set(news_list)
        logger.info(f"Pushed {len(news_list)} news items to {path}")
    except Exception as e:
        logger.error(f"Error updating realtime news: {e}")

def update_realtime_stats(stats, query=None):
    """
    Pushes statistics updates to Firebase Realtime Database.
    """
    try:
        path = f"live/stats/{query}" if query else "live/stats/general"
        ref = db.reference(path)
        ref.set(stats)
        logger.info(f"Pushed stats to {path}")
    except Exception as e:
        logger.error(f"Error updating realtime stats: {e}")
def update_last_active():
    """Update the system's last active timestamp in Firebase."""
    try:
        ref = db.reference("system/last_active")
        ref.set(time.time())
    except Exception as e:
        logger.error(f"Error updating last active: {e}")

def get_last_active():
    """Retrieve the system's last active timestamp from Firebase."""
    try:
        ref = db.reference("system/last_active")
        return ref.get()
    except Exception as e:
        logger.error(f"Error getting last active: {e}")
        return 0

import time
