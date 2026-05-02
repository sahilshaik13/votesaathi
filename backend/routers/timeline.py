from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Timeline"])

@router.get("/timeline")
def get_timeline(type: str = "general"):
    # Placeholder timeline data
    phases = [
        {"name": "Announcement", "description": "Election dates announced by ECI", "duration": "Day 0"},
        {"name": "Nomination", "description": "Candidates file papers", "duration": "Day 7-14"}
    ]
    return {"phases": phases}
