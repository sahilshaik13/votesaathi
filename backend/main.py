from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, timeline, health

app = FastAPI(title="VoteSaathi API", description="Backend for the VoteSaathi Election Assistant", version="1.0.0")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(timeline.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
