import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch the secret dynamically from config (which uses Secret Manager)
from config import JWT_SECRET_KEY, JWT_ALGORITHM

def create_token(user_id: str) -> str:
    """Create a simple JWT for the given user_id."""
    payload = {
        "sub": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> str | None:
    """Verify the JWT and return the user_id (sub)."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None
