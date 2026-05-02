"""
Firestore service — reads and writes chat session history.

All operations use Application Default Credentials (ADC) automatically when
running locally (via `gcloud auth application-default login`) or on Cloud Run.
"""

from google.cloud import firestore
from config import GCP_PROJECT_ID, FIRESTORE_COLLECTION


def _client() -> firestore.Client:
    return firestore.Client(project=GCP_PROJECT_ID)


def get_session_history(session_id: str) -> list[dict]:
    """Return ordered list of messages for a session, or [] if none."""
    db = _client()
    doc = db.collection(FIRESTORE_COLLECTION).document(session_id).get()
    if doc.exists:
        return doc.to_dict().get("history", [])
    return []


def append_message(session_id: str, role: str, content: str) -> None:
    """Append a single message turn to the session document."""
    db = _client()
    ref = db.collection(FIRESTORE_COLLECTION).document(session_id)
    ref.set(
        {"history": firestore.ArrayUnion([{"role": role, "content": content}])},
        merge=True,
    )


def delete_session(session_id: str) -> None:
    """Delete the session document from Firestore."""
    db = _client()
    db.collection(FIRESTORE_COLLECTION).document(session_id).delete()
