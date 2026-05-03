from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import uvicorn
import os
import logging
import time

from routers import dashboard

app = FastAPI(title="VoteSaathi Scraper Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ScraperService")


@app.get("/")
async def health():
    return {"status": "VoteSaathi Scraper is running", "version": "1.0.0"}


def background_scraper():
    logger.info("Background scraper thread started (Always On).")

    while True:
        try:
            from live_scraper_process import run_scraper_cycle

            logger.info("Running scheduled scraper cycle...")
            run_scraper_cycle()
            time.sleep(120)  # Wait 2 minutes between cycles
        except Exception as e:
            logger.error(f"Error in scraper loop: {e}")
            time.sleep(60)


if __name__ == "__main__":
    # Start scraper background thread
    t = threading.Thread(target=background_scraper, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
