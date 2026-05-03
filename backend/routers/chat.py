from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
import uuid

from services.firestore_service import get_session_history, append_message, delete_session, get_user_sessions
from services.auth_service import create_token, verify_token
from agent.election_agent import run_agent

router = APIRouter(prefix="/api", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    user_id: str | None = None
    lang: str | None = "English"


class ChatResponse(BaseModel):
    reply: str
    sources: list
    session_id: str


from services.realtime_service import update_last_active

@router.post("/chat", response_model=ChatResponse)
async def post_chat(request: ChatRequest, authorization: str | None = Header(None)):
    # Track activity
    update_last_active()
    
    session_id = request.session_id or str(uuid.uuid4())
    user_id = request.user_id
    lang = request.lang or "English"

    # Verify token if user_id is provided
    if user_id and authorization:
        token = authorization.replace("Bearer ", "")
        sub = verify_token(token)
        if sub != user_id:
            # For now, just log and continue to avoid blocking the user
            print(f"DEBUG: Token mismatch! sub={sub}, user_id={user_id}")
            # raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Fetch history from Firestore
    history = get_session_history(session_id)

    # Run the agent with language context
    result = run_agent(request.message, history, lang=lang)

    # Persist both turns to Firestore with user_id mapping
    append_message(session_id, "user", request.message, user_id=user_id)
    append_message(session_id, "assistant", result["text"], user_id=user_id)

    return ChatResponse(reply=result["text"], sources=result["sources"], session_id=session_id)


class HeartbeatResponse(BaseModel):
    status: str

class SessionListResponse(BaseModel):
    sessions: list

class TokenResponse(BaseModel):
    token: str

class HistoryResponse(BaseModel):
    history: list

class DeleteResponse(BaseModel):
    deleted: bool

@router.post("/heartbeat", response_model=HeartbeatResponse)
async def heartbeat():
    """
    Signals that the user is still active to keep the background scraper running.
    """
    update_last_active()
    return HeartbeatResponse(status="ok")


@router.get("/user/sessions/{user_id}", response_model=SessionListResponse)
async def list_user_sessions(user_id: str, authorization: str | None = Header(None)):
    """
    Retrieves all chat session metadata associated with a specific user ID.
    """
    # Verify token
    if authorization:
        token = authorization.replace("Bearer ", "")
        sub = verify_token(token)
        if sub != user_id:
            print(f"DEBUG: Session list token mismatch! sub={sub}, user_id={user_id}")
            
    sessions = get_user_sessions(user_id)
    return SessionListResponse(sessions=sessions)


@router.get("/user/token/{user_id}", response_model=TokenResponse)
async def get_token(user_id: str):
    """
    Generates a secure JWT for a user ID (Loginless Auth).
    """
    token = create_token(user_id)
    return TokenResponse(token=token)


@router.get("/session/{session_id}", response_model=HistoryResponse)
async def get_session(session_id: str):
    """
    Fetches the full message history for a specific chat session.
    """
    history = get_session_history(session_id)
    return HistoryResponse(history=history)


@router.delete("/session/{session_id}", response_model=DeleteResponse)
async def delete_session_route(session_id: str):
    """
    Permanently removes a chat session and its history from Firestore.
    """
    delete_session(session_id)
    return DeleteResponse(deleted=True)
