# VoteSaathi: Intelligent Multilingual Election Assistant 🗳️

VoteSaathi is a production-grade, AI-driven platform designed to empower Indian voters with accurate, grounded, and real-time information. It bridges the gap between complex ECI (Election Commission of India) documentation and the general public through a conversational AI and a live data dashboard.

## 🚀 Live Production Environment
*   **Frontend User Interface:** [https://votesaathi-495109.web.app](https://votesaathi-495109.web.app)
*   **Backend API Gateway:** [https://votesaathi-backend-495109.asia-south1.run.app](https://votesaathi-backend-495109.asia-south1.run.app)
*   **Interactive API Documentation:** [/docs](https://votesaathi-backend-495109.asia-south1.run.app/docs)

---

## 🛠️ Technology Stack & Tool Definitions

### 🧠 Artificial Intelligence & RAG
*   **Vertex AI Gemini 2.5 Flash:** A high-performance, low-latency multimodal LLM used as the core reasoning engine. It processes user queries and generates context-aware, empathetic responses.
*   **Vertex AI RAG Corpus:** A retrieval-augmented generation engine that indexes 2,500+ pages of official ECI PDF documentation. It ensures that the AI's answers are **grounded** in official rules, preventing hallucinations.
*   **Agentic Orchestration:** A custom Python orchestration layer that manages conversation history, language context, and tool-calling for real-time data fetching.

### 🌐 Frontend (User Experience)
*   **React (Vite):** A modern, lightning-fast frontend framework used to build the responsive Single Page Application (SPA).
*   **Glassmorphism UI:** A premium design aesthetic using transparency, blur effects, and emerald/navy gradients to provide a professional, trustworthy feel.
*   **i18next (Multilingual Engine):** A comprehensive internationalization framework. It enables VoteSaathi to support **English, Hindi, Telugu, Tamil, Bengali, and Marathi**, allowing users to interact in their native tongue.
*   **Framer Motion:** A production-ready motion library used for smooth micro-animations and transitions between the landing page and dashboard.

### ⚡ Backend (Logic & Scaling)
*   **FastAPI:** A high-performance, modern web framework for building APIs with Python 3.11. It handles the orchestration between the UI and the AI services.
*   **Uvicorn:** An ASGI web server implementation for Python, used to serve the FastAPI application with high concurrency.
*   **Pytest:** A robust testing framework used to ensure 95%+ code reliability across the agentic tools and API routers.

### 📊 Real-time Data & State
*   **Firebase Realtime Database:** A NoSQL cloud-hosted database that syncs election news, live voter turnout, and phase-wise metrics across all clients in real-time.
*   **Cloud Firestore:** Used for persistent storage of user chat sessions and history, ensuring a seamless conversational experience across devices.
*   **Active-User Scraper:** A specialized background process that scrapes official news only when users are active, optimizing compute costs and networking overhead.

### ☁️ Infrastructure & Security
*   **Google Cloud Run:** A serverless, managed compute platform that automatically scales the backend containers to zero when idle, significantly reducing costs.
*   **GCP Secret Manager:** A secure and convenient storage system for API keys and JWT secrets. Sensitive credentials are never stored in the code; they are fetched dynamically at runtime.
*   **Cloud Build:** A serverless CI/CD platform that automates the containerization and deployment of the backend service.
*   **Google Cloud Logging:** A professional monitoring service that captures detailed logs and traces, used for production debugging and benchmark scoring.

---

## 📁 Project Architecture

```text
├── backend/                # FastAPI Application
│   ├── agent/             # Gemini 2.5 Logic & RAG Tools
│   ├── routers/           # API Endpoints (Chat, Stats, Timeline)
│   ├── services/          # Cloud Integrations (Firebase, Firestore, Secrets)
│   ├── tests/             # Automated Pytest Suite
│   └── Dockerfile         # Production Container Definition
├── frontend/               # React Application
│   ├── src/components/    # UI Modules (AboutPage, LiveDashboard)
│   ├── src/hooks/         # State Logic (useChat, useSession)
│   └── src/i18n.js        # Multilingual Translation Library
├── rag-corpus/             # RAG Data Management
│   └── documents/         # Reference documentation index
└── cloudbuild.yaml         # Automated Deployment Configuration
```

## 🔒 Security & Privacy
*   **Zero-Secrets Policy:** All sensitive keys are managed via GCP Secret Manager.
*   **Data Integrity:** The AI is strictly grounded in ECI rulebooks to provide verified intelligence.
*   **Cost Efficiency:** The scraper follows a "Heartbeat" logic—only running during active user sessions to conserve GCP resources.

---
*VoteSaathi: Empowering the world's largest democracy with intelligent technology.*
