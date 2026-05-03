import firebase_admin
from firebase_admin import credentials, db
from config import FIREBASE_DATABASE_URL
import logging
import time
import os

logger = logging.getLogger(__name__)

# Initialize Firebase Admin once with Application Default Credentials (Cloud Run)
try:
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path and os.path.exists(cred_path):
            logger.info(f"Initializing Firebase with credentials from {cred_path}")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})
        else:
            logger.info("Initializing Firebase with Application Default Credentials")
            firebase_admin.initialize_app(options={'databaseURL': FIREBASE_DATABASE_URL})
except Exception as e:
    logger.error(f"Non-blocking Firebase initialization error: {e}")


def update_realtime_news(news_list, query=None):
    """Pushes news updates to Firebase Realtime Database."""
    try:
        path = f"live/news/{query}" if query else "live/news/general"
        ref = db.reference(path)
        ref.set(news_list)
        logger.info(f"Pushed {len(news_list)} news items to {path}")
    except Exception as e:
        logger.error(f"Error updating realtime news: {e}")


def update_realtime_stats(stats, query=None):
    """Pushes statistics updates to Firebase Realtime Database."""
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
