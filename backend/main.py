"""
VoteSaathi API — FastAPI application entry point.

Registers all routers and configures CORS for the election assistant backend.
"""

import google.cloud.logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, timeline, health, dashboard

# Initialize Google Cloud Logging with extreme safety
try:
    import google.cloud.logging
    client = google.cloud.logging.Client()
    client.setup_logging()
except Exception as e:
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Google Cloud Logging could not be initialized (falling back to standard): {e}")

app = FastAPI(
    title="VoteSaathi API",
    description="Backend for the VoteSaathi Election Assistant — powered by Vertex AI Gemini & ADK",
    version="1.0.0",
)

# CORS config
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import threading
import time
import logging

# We import these inside the task to avoid circular imports or early failures
def scraper_background_task():
    """Background task to run the scraper periodically if users are active."""
    logger = logging.getLogger("ScraperThread")
    logger.info("Background scraper thread initializing...")
    
    # Give the main app time to settle
    time.sleep(10)
    
    while True:
        try:
            from live_scraper_process import run_scraper_cycle, get_last_active
            last_active = get_last_active() or 0
            time_since_active = time.time() - last_active
            
            if time_since_active < 600: # 10 minutes
                logger.info("Active users detected. Running scraper cycle...")
                run_scraper_cycle()
                time.sleep(120)
            else:
                time.sleep(60)
        except Exception as e:
            logging.error(f"Error in background scraper thread: {e}")
            time.sleep(60)

@app.on_event("startup")
async def startup_event():
    try:
        thread = threading.Thread(target=scraper_background_task, daemon=True)
        thread.start()
        logging.info("Scraper background thread launched successfully.")
    except Exception as e:
        logging.error(f"Failed to launch scraper thread: {e}")

# Register routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(timeline.router)
app.include_router(dashboard.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
