from pydantic import BaseModel
from typing import List, Optional, Union

class NewsItem(BaseModel):
    title: str
    link: str
    pub_date: str
    source: str

class StateInfo(BaseModel):
    name: str
    total_seats: int
    voter_turnout: str

class LiveStats(BaseModel):
    phase: str
    voter_turnout: str
    registered_voters: str
    polling_stations: str
    total_seats: str

class DashboardData(BaseModel):
    news: List[NewsItem]
    stats: LiveStats

class ConstituencyData(BaseModel):
    name: str
    state: str
    candidates: Union[int, str]
    phase: Union[int, str]
    last_turnout: str

class SearchResponse(BaseModel):
    found: bool
    data: Optional[ConstituencyData] = None
    message: Optional[str] = None
