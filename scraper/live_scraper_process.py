import time
import logging
from services.scraper_service import scrape_live_election_news, get_live_stats
from services.realtime_service import update_realtime_news, update_realtime_stats, get_last_active

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("LiveScraper")

# Every State and UT in India
ALL_LOCATIONS = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", 
    "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa", 
    "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", 
    "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", 
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab", "Rajasthan", 
    "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

# Trending Election Topics
HOT_TOPICS = [
    "EVM VVPAT", "Voter Turnout", "Election Manifesto", "Model Code of Conduct", 
    "Election Commission of India", "Voter ID Card", "Polling Booth"
]

def run_scraper_cycle():
    """
    Performs one full cycle of scraping and updating Firebase.
    """
    logger.info("Starting comprehensive scraper cycle...")
    
    # 1. Update General News & Stats
    general_news = scrape_live_election_news(lang="en")
    general_stats = get_live_stats()
    update_realtime_news(general_news)
    update_realtime_stats(general_stats)
    
    # 2. Update All Locations News
    for loc in ALL_LOCATIONS:
        loc_news = scrape_live_election_news(lang="en", query=loc)
        update_realtime_news(loc_news, query=f"states/{loc}")
        time.sleep(1) # Be polite to RSS servers
    
    # 3. Update Hot Topics
    for topic in HOT_TOPICS:
        topic_news = scrape_live_election_news(lang="en", query=topic)
        update_realtime_news(topic_news, query=f"topics/{topic.replace(' ', '_')}")
        time.sleep(1)
    
    logger.info("Comprehensive scraper cycle complete.")

if __name__ == "__main__":
    logger.info("Realtime Election Scraper started (Always On).")
    
    while True:
        try:
            run_scraper_cycle()
            # Wait for 2 minutes before next cycle
            logger.info("Waiting 2 minutes for next cycle...")
            time.sleep(120) 
        except KeyboardInterrupt:
            logger.info("Scraper stopped by user.")
            break
        except Exception as e:
            logger.error(f"Error in scraper loop: {e}")
            time.sleep(60)
