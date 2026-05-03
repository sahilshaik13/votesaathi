"""
VoteSaathi API — FastAPI application entry point.

Registers all routers and configures CORS for the election assistant backend.
"""

import google.cloud.logging
import os
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
# Include both the production frontend and localhost for development
allowed_origins = [
    "https://votesaathi-frontend-171624099766.asia-south1.run.app",
    "https://votesaathi-495109.web.app", # Firebase hosting fallback
    "http://localhost:5173",
    "http://localhost:3000"
]
# Add any origins from environment variables
env_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
allowed_origins.extend([o for o in env_origins if o])

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.middleware("http")
async def emergency_cors_and_error_handler(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
        
    try:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    except Exception as e:
        import logging
        logging.error(f"Unhandled exception in request: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

import threading
@app.get("/")
async def root():
    return {"message": "VoteSaathi API is Live", "version": "1.0.0"}

# Register routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(timeline.router)
app.include_router(dashboard.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
