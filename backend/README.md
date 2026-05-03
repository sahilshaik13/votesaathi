# VoteSaathi Backend — Election Intelligence Engine

VoteSaathi is a sophisticated AI-powered election assistant designed to help Indian citizens navigate the electoral process with precision and transparency.

## 🚀 Key Features
- **Grounded AI (RAG)**: Utilizes Vertex AI RAG Engine to retrieve information exclusively from official Election Commission of India (ECI) PDFs.
- **Multilingual Intelligence**: Native support for 7+ Indian languages (Hindi, Telugu, Tamil, Bengali, Marathi, etc.).
- **Real-time Election Dashboard**: Live tracking of voter turnout, news, and election phases via Firebase Realtime Database.
- **Active-User Scraper**: An intelligent scraping engine that only operates when users are active to optimize costs and storage.
- **Security First**: All sensitive keys managed via Google Cloud Secret Manager.

## 🏗️ Architecture
- **Framework**: FastAPI (Python 3.11)
- **AI Stack**: Gemini 2.5 Flash + Vertex AI Search
- **Database**: Firebase RTDB (Live Data) + Firestore (Chat History)
- **Deployment**: Google Cloud Run (Serverless)
- **Monitoring**: Google Cloud Logging

## 🛠️ Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set up `.env` with your GCP Project ID and Corpus ID.
3. Run the dev server: `python main.py`

## 🧪 Testing
Run the automated test suite:
```bash
pytest
```
