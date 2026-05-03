import jwt
import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter(prefix="/api/auth", tags=["Auth"])
security = HTTPBearer()

def create_jwt_token(user_id: str) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@router.post("/token")
def login_anonymous():
    """Generate an anonymous JWT token for a new session/user."""
    user_id = str(uuid.uuid4())
    token = create_jwt_token(user_id)
    return {"access_token": token, "token_type": "bearer", "user_id": user_id}
