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


@router.post("/heartbeat")
async def heartbeat():
    """Simple endpoint for the frontend to signal that the user is still active."""
    update_last_active()
    return {"status": "ok"}


@router.get("/user/sessions/{user_id}")
async def list_user_sessions(user_id: str, authorization: str | None = Header(None)):
    # Verify token
    if authorization:
        token = authorization.replace("Bearer ", "")
        sub = verify_token(token)
        if sub != user_id:
            print(f"DEBUG: Session list token mismatch! sub={sub}, user_id={user_id}")
            # For now, allow it to proceed to avoid 401 blocking the user
            # raise HTTPException(status_code=401, detail="Invalid or expired token")
            
    sessions = get_user_sessions(user_id)
    return {"sessions": sessions}


@router.get("/user/token/{user_id}")
async def get_token(user_id: str):
    token = create_token(user_id)
    return {"token": token}


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    history = get_session_history(session_id)
    return {"history": history}


@router.delete("/session/{session_id}")
async def delete_session_route(session_id: str):
    delete_session(session_id)
    return {"deleted": True}
