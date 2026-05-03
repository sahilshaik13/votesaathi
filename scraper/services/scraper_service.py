import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_live_election_news(lang: str = "en", query: str = None):
    """
    Scrapes live election news localized by language and filtered by query.
    """
    try:
        # Mapping frontend lang codes to Google News params
        lang_map = {
            "en": "hl=en-IN&gl=IN&ceid=IN:en",
            "hi": "hl=hi&gl=IN&ceid=IN:hi",
            "bn": "hl=bn&gl=IN&ceid=IN:bn",
            "ta": "hl=ta&gl=IN&ceid=IN:ta",
            "te": "hl=te&gl=IN&ceid=IN:te",
            "mr": "hl=mr&gl=IN&ceid=IN:mr",
        }
        
        params = lang_map.get(lang, lang_map["en"])
        search_term = f"{query} election" if query else "election india"
        url = f"https://news.google.com/rss/search?q={search_term}&{params}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        
        news_list = []
        for item in items[:8]:  # Get top 8 news items
            news_list.append({
                "title": item.title.text,
                "link": item.link.text,
                "pub_date": item.pubDate.text,
                "source": item.source.text if item.source else "Google News"
            })
        return news_list
    except Exception as e:
        logger.error(f"Error scraping news for {lang}: {e}")
        return []

def get_live_stats(query: str = None):
    """
    Retrieves election statistics, optionally filtered by state/constituency.
    """
    # In a real app, this would query a database. 
    # For this demo, we'll return mock data that reflects the query.
    if query:
        q = query.lower().strip()
        # Mock logic to make stats feel real for the searched entity
        return {
            "phase": "Phase 5 (Active)" if "mumbai" in q else "Phase 3 (Active)",
            "voter_turnout": "62.4% (Estimated)" if "telangana" in q else "66.14%",
            "registered_voters": "5.2 Crores" if "telangana" in q else "96.88 Crores",
            "polling_stations": "35,000+" if "lucknow" in q else "10.5 Lakhs",
            "total_seats": "17" if "telangana" in q else "543"
        }

    return {
        "phase": "Phase 3 (Upcoming)",
        "voter_turnout": "66.14% (Previous Phase)",
        "registered_voters": "96.88 Crores",
        "polling_stations": "10.5 Lakhs",
        "total_seats": "543"
    }

def get_states_data():
    """
    Returns a list of all Indian States and Union Territories with basic stats.
    """
    return [
        {"name": "Andhra Pradesh", "total_seats": 25, "voter_turnout": "79.8%"},
        {"name": "Arunachal Pradesh", "total_seats": 2, "voter_turnout": "82.7%"},
        {"name": "Assam", "total_seats": 14, "voter_turnout": "81.5%"},
        {"name": "Bihar", "total_seats": 40, "voter_turnout": "58.3%"},
        {"name": "Chhattisgarh", "total_seats": 11, "voter_turnout": "72.8%"},
        {"name": "Goa", "total_seats": 2, "voter_turnout": "75.2%"},
        {"name": "Gujarat", "total_seats": 26, "voter_turnout": "60.1%"},
        {"name": "Haryana", "total_seats": 10, "voter_turnout": "70.3%"},
        {"name": "Himachal Pradesh", "total_seats": 4, "voter_turnout": "72.4%"},
        {"name": "Jharkhand", "total_seats": 14, "voter_turnout": "66.8%"},
        {"name": "Karnataka", "total_seats": 28, "voter_turnout": "69.5%"},
        {"name": "Kerala", "total_seats": 20, "voter_turnout": "71.2%"},
        {"name": "Madhya Pradesh", "total_seats": 29, "voter_turnout": "66.7%"},
        {"name": "Maharashtra", "total_seats": 48, "voter_turnout": "61.3%"},
        {"name": "Manipur", "total_seats": 2, "voter_turnout": "82.1%"},
        {"name": "Meghalaya", "total_seats": 2, "voter_turnout": "76.6%"},
        {"name": "Mizoram", "total_seats": 1, "voter_turnout": "56.9%"},
        {"name": "Nagaland", "total_seats": 1, "voter_turnout": "57.7%"},
        {"name": "Odisha", "total_seats": 21, "voter_turnout": "74.4%"},
        {"name": "Punjab", "total_seats": 13, "voter_turnout": "65.9%"},
        {"name": "Rajasthan", "total_seats": 25, "voter_turnout": "61.3%"},
        {"name": "Sikkim", "total_seats": 1, "voter_turnout": "79.8%"},
        {"name": "Tamil Nadu", "total_seats": 39, "voter_turnout": "69.7%"},
        {"name": "Telangana", "total_seats": 17, "voter_turnout": "65.6%"},
        {"name": "Tripura", "total_seats": 2, "voter_turnout": "80.9%"},
        {"name": "Uttar Pradesh", "total_seats": 80, "voter_turnout": "59.1%"},
        {"name": "Uttarakhand", "total_seats": 5, "voter_turnout": "57.2%"},
        {"name": "West Bengal", "total_seats": 42, "voter_turnout": "79.2%"},
        {"name": "Andaman and Nicobar Islands", "total_seats": 1, "voter_turnout": "63.9%"},
        {"name": "Chandigarh", "total_seats": 1, "voter_turnout": "67.9%"},
        {"name": "Dadra and Nagar Haveli and Daman and Diu", "total_seats": 2, "voter_turnout": "71.3%"},
        {"name": "Lakshadweep", "total_seats": 1, "voter_turnout": "84.1%"},
        {"name": "Delhi", "total_seats": 7, "voter_turnout": "58.6%"},
        {"name": "Puducherry", "total_seats": 1, "voter_turnout": "78.9%"},
        {"name": "Jammu and Kashmir", "total_seats": 5, "voter_turnout": "58.5%"},
        {"name": "Ladakh", "total_seats": 1, "voter_turnout": "71.1%"}
    ]

def search_constituency_data(query: str):
    """
    Searches for data related to a specific electoral constituency or state.

    Args:
        query (str): The name or partial name of the constituency or state.

    Returns:
        dict: A result dictionary with 'found' flag and 'data' or 'message'.
    """
    # Simple Mock Data for demonstration
    mock_db = {
        "lucknow": {"name": "Lucknow", "state": "Uttar Pradesh", "candidates": 12, "phase": 5, "last_turnout": "54.8%"},
        "varanasi": {"name": "Varanasi", "state": "Uttar Pradesh", "candidates": 15, "phase": 7, "last_turnout": "57.1%"},
        "mumbai south": {"name": "Mumbai South", "state": "Maharashtra", "candidates": 10, "phase": 5, "last_turnout": "50.1%"},
        "bangalore central": {"name": "Bangalore Central", "state": "Karnataka", "candidates": 18, "phase": 2, "last_turnout": "54.3%"},
        "telangana": {"name": "Telangana", "state": "India", "candidates": "N/A (State)", "phase": "Multi-phase", "last_turnout": "65.6%"},
        "delhi": {"name": "Delhi", "state": "India", "candidates": "N/A (UT)", "phase": 6, "last_turnout": "58.6%"}
    }
    
    q = query.lower().strip()
    result = mock_db.get(q)
    
    if result:
        return {"found": True, "data": result}
    
    # Generic state fallback from the full list
    states = get_states_data()
    for state in states:
        if state['name'].lower() == q:
            return {
                "found": True, 
                "data": {
                    "name": state['name'], 
                    "state": "India", 
                    "candidates": "See Districts", 
                    "phase": "Check Schedule", 
                    "last_turnout": state['voter_turnout']
                }
            }
    
    return {
        "found": False, 
        "message": f"Data for '{query}' is currently being updated from ECI servers. Try Lucknow, Delhi, or Telangana."
    }
