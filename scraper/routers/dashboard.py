from fastapi import APIRouter
from services.scraper_service import (
    scrape_live_election_news,
    get_live_stats,
    search_constituency_data,
    get_states_data
)
from typing import List, Optional
import os

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

from services.realtime_service import update_last_active

@router.get("/live")
async def get_live_dashboard_data(lang: str = "en", query: Optional[str] = None):
    """Fetches live news and statistics for the election dashboard."""
    # Keep the background scraper awake since a user is viewing the dashboard
    update_last_active()
    
    news = scrape_live_election_news(lang, query=query)
    stats = get_live_stats(query=query)
    return {"news": news, "stats": stats}

@router.get("/search")
async def find_constituency(query: Optional[str] = None, lat: Optional[float] = None, lng: Optional[float] = None):
    """Searches for specific constituency data."""
    if not query and lat and lng:
        query = "Hyderabad" if (17 < lat < 18 and 78 < lng < 79) else "Lucknow"
    return search_constituency_data(query or "")

@router.get("/states")
async def get_all_states():
    """Returns a list of all Indian States and UTs with basic election metadata."""
    return get_states_data()

@router.get("/state-briefing")
async def get_state_briefing(state: str):
    """
    Generates a comprehensive, neutral election briefing for a specific state
    using Gemini's built-in knowledge (no tool restrictions).
    """
    try:
        from google import genai
        from google.genai import types

        project = os.environ.get("GCP_PROJECT_ID", "votesaathi-495109")
        location = os.environ.get("GCP_LOCATION", "us-central1")
        model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-001")

        client = genai.Client(vertexai=True, project=project, location=location)

        prompt = f"""Provide a comprehensive, neutral election briefing for the Indian state of {state}.

Please include:
1. **Major Political Parties**: Key parties that contest elections in {state}, their symbols and current standing
2. **Current Government**: Who is the ruling party/coalition and Chief Minister (as of your knowledge)
3. **Electoral Profile**: Total Lok Sabha/Vidhan Sabha seats, voter statistics
4. **Recent Election Results**: Brief summary of the most recent state or general election results for {state}
5. **Key Issues**: Top 3 electoral issues in the state
6. **Upcoming Schedule**: Any known upcoming election dates or schedules (note if unknown)

Be factual, neutral, and cite eci.gov.in for verification. Do NOT express political opinions or endorsements."""

        config = types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=1500,
        )

        response = client.models.generate_content(
            model=model,
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=config,
        )

        briefing_text = response.candidates[0].content.parts[0].text

        return {
            "state": state,
            "briefing": briefing_text.strip(),
            "sources": [{"source_uri": "https://eci.gov.in", "text": "Election Commission of India"}]
        }

    except Exception as e:
        return {
            "state": state,
            "briefing": f"Unable to generate briefing for {state} at this time. Please visit eci.gov.in for official information.",
            "sources": [],
            "error": str(e)
        }
