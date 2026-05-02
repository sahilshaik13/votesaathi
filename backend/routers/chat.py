from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/api", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    sources: list
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def post_chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    # Placeholder for agent invocation
    reply = "This is a placeholder response from VoteSaathi."
    sources = []
    return ChatResponse(reply=reply, sources=sources, session_id=session_id)

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    # Placeholder for Firestore fetch
    return {"history": []}

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    # Placeholder for Firestore delete
    return {"deleted": True}
