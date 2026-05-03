from fastapi import APIRouter
from services.scraper_service import (
    scrape_live_election_news, 
    get_live_stats, 
    search_constituency_data,
    get_states_data
)
from agent.election_agent import run_agent
from schemas.dashboard import DashboardData, SearchResponse, StateInfo
from typing import List, Optional

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/live", response_model=DashboardData)
async def get_live_dashboard_data(lang: str = "en", query: Optional[str] = None):
    """
    Fetches live news and statistics for the election dashboard.

    Args:
        lang (str): The language code for news localization.
        query (str, optional): A search term (state/constituency) to filter results.

    Returns:
        DashboardData: A validated object containing a list of news items and key stats.
    """
    news = scrape_live_election_news(lang, query=query)
    stats = get_live_stats(query=query)
    return {
        "news": news,
        "stats": stats
    }

@router.get("/search", response_model=SearchResponse)
async def find_constituency(query: Optional[str] = None, lat: Optional[float] = None, lng: Optional[float] = None):
    """
    Searches for specific constituency data via the backend service.

    Args:
        query (str, optional): The name of the constituency to search for.
        lat (float, optional): Latitude for geolocation search.
        lng (float, optional): Longitude for geolocation search.

    Returns:
        SearchResponse: A validated object containing search results or an error message.
    """
    if not query and lat and lng:
        # Mocking a search query based on coordinates for demonstration
        query = "Hyderabad" if (17 < lat < 18 and 78 < lng < 79) else "Lucknow"
    
    return search_constituency_data(query or "")

@router.get("/states", response_model=List[StateInfo])
async def get_all_states():
    """
    Returns a list of all Indian States and UTs with basic election metadata.
    """
    return get_states_data()

@router.get("/state-briefing")
async def get_state_briefing(state: str):
    """
    Generates a comprehensive, neutral election briefing for a specific state 
    using the VoteSaathi AI agent.
    """
    prompt = f"Provide a comprehensive, neutral election briefing for the state of {state}. Include major political parties, key current ministers (neutral overview), ECI rules specific to this region, and upcoming election schedule. Keep it purely informational."
    
    # Run the agent turn (no history for dashboard briefing)
    result = run_agent(prompt, [])
    return {
        "state": state,
        "briefing": result["text"],
        "sources": result["sources"]
    }
