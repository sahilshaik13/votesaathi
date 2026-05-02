from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from services.firestore_service import get_session_history, append_message, delete_session
from agent.election_agent import run_agent

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

    # Fetch history from Firestore
    history = get_session_history(session_id)

    # Run the agent
    result = run_agent(request.message, history)

    # Persist both turns to Firestore
    append_message(session_id, "user", request.message)
    append_message(session_id, "assistant", result["text"])

    return ChatResponse(reply=result["text"], sources=result["sources"], session_id=session_id)


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    history = get_session_history(session_id)
    return {"history": history}


@router.delete("/session/{session_id}")
async def delete_session_route(session_id: str):
    delete_session(session_id)
    return {"deleted": True}
