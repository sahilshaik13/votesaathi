# VoteSaathi Backend

FastAPI backend for VoteSaathi, an Election Process Assistant.

## Setup

1. Configure Google Application Default Credentials:
   ```bash
   gcloud auth application-default login
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run locally:
   ```bash
   uvicorn main:app --reload
   ```

## Architecture

- **`routers/`**: Contains the API endpoints (`chat`, `health`, `timeline`).
- **`agent/`**: (To be implemented) ADK LlmAgent logic and tools.
- **`services/`**: (To be implemented) Firestore and RAG integrations.
