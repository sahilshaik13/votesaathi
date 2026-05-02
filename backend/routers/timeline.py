from fastapi import APIRouter
from agent.tools.get_timeline import get_election_timeline

router = APIRouter(prefix="/api", tags=["Timeline"])


@router.get("/timeline")
def get_timeline(type: str = "general"):
    phases = get_election_timeline(type)
    return {"phases": phases}
