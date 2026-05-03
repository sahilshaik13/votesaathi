import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_live_election_news(lang: str = "en", query: str = None):
    try:
        lang_map = {
            "en": "hl=en-IN&gl=IN&ceid=IN:en"
        }
        params = lang_map.get(lang, lang_map["en"])
        search_term = f"{query} election" if query else "election india"
        url = f"https://news.google.com/rss/search?q={search_term}&{params}"
        
        print(f"Fetching URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        print(f"Found {len(items)} items")
        
        news_list = []
        for item in items[:8]:
            news_list.append({
                "title": item.title.text,
                "link": item.link.text,
                "pub_date": item.pubDate.text,
                "source": item.source.text if item.source else "Google News"
            })
        return news_list
    except Exception as e:
        print(f"Exception: {e}")
        return []

print(scrape_live_election_news())
