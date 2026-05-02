# 🗳️ VoteSaathi — Election Process Assistant
### PromptWars by Google | Challenge Submission

---

## ✦ Face Page

### What is VoteSaathi?

**VoteSaathi** (meaning *Vote Companion* in Hindi) is a conversational AI assistant that helps Indian citizens — first-time voters, general public, students, and researchers — understand the Indian election process in a clear, interactive, and grounded way.

Built entirely on **Google Cloud Platform**, VoteSaathi combines a **Vertex AI Gemini-powered ADK agent** with a **RAG Engine** trained on real Election Commission of India documents, giving users accurate, contextual, and jargon-free answers about elections.

---

### Challenge Vertical
**Civic Education & Public Service Assistant**

---

### How VoteSaathi Meets the Challenge

| Expectation | How VoteSaathi Delivers |
|---|---|
| **Smart, dynamic assistant** | ADK `LlmAgent` with tool-calling — dynamically decides whether to search RAG, explain a step, or give a timeline |
| **Logical decision-making** | Agent routes user intent to the right tool (timeline, step explainer, FAQ, voter eligibility checker) |
| **Effective use of Google Services** | Vertex AI Gemini 2.5 Flash, ADK, RAG Engine, Cloud Run, Firestore, Firebase Hosting, Secret Manager, Cloud Build |
| **Real-world usability** | Targets actual Indian voters; answers questions like "How do I register?", "When is the next election?", "What is Model Code of Conduct?" |
| **Clean & maintainable code** | Modular FastAPI backend with separated agent, tool, and route layers; Vite React frontend with component-first architecture |

---

### Evaluation Alignment

| Focus Area | Implementation |
|---|---|
| **Code Quality** | FastAPI routers separated by concern; ADK tools as independent Python modules; React components scoped and reusable |
| **Security** | API keys in Secret Manager; Firestore rules; CORS policy on Cloud Run; no PII stored |
| **Efficiency** | Gemini Flash (low latency, cost-optimized); RAG retrieval limits tokens; Cloud Run scales to zero |
| **Testing** | Pytest for FastAPI routes + agent tools; Vitest for React components; ADK eval harness for agent quality |
| **Accessibility** | ARIA labels, keyboard nav, contrast-compliant UI, multilingual-ready prompts (Hindi support planned) |
| **Google Services** | 7+ GCP services meaningfully integrated — not cosmetic usage |

---

---

## 1. Product Overview

| Field | Detail |
|---|---|
| **Name** | VoteSaathi |
| **Type** | Conversational AI Web App |
| **Stack** | React + Vite (frontend) · FastAPI Python (backend) · Google ADK + Vertex AI Gemini 2.5 Flash (agent) · Vertex AI RAG Engine (retrieval) |
| **Hosting** | Firebase Hosting (frontend) · Cloud Run (backend) |
| **Purpose** | Help Indian citizens understand election processes, voter registration, timelines, ECI rules, and FAQs through a grounded, agentic AI chat interface |

---

## 2. Problem Statement

India conducts the world's largest democratic elections, yet millions of citizens — especially first-time voters — lack accessible, easy-to-understand information about the process. Official Election Commission of India (ECI) resources exist but are dense, scattered, and difficult to navigate. Misinformation about voter ID, eligibility, deadlines, and voting procedures is widespread on social media.

There is no intelligent, conversational interface that can answer a voter's specific question in plain language, grounded in official ECI documentation, in real time.

---

## 3. Goals

- Provide accurate, grounded answers about Indian elections via an AI chat interface
- Cover the full election lifecycle: announcement → nomination → campaigning → voting → results → government formation
- Support first-time voters with step-by-step guidance (voter registration, EPIC card, polling booth lookup)
- Ground all responses in official ECI documents via Vertex AI RAG Engine
- Deploy a fully serverless, production-ready app on GCP
- Demonstrate meaningful use of ≥5 GCP services

---

## 4. Non-Goals

- Not a real-time election results tracker
- Not a multilingual translation service (Hindi UI is a stretch goal, not core)
- Not a political opinion or candidate recommendation tool
- Not a voter database — no PII collection
- Not supporting elections outside India in v1

---

## 5. User Flow

```
User opens VoteSaathi (Firebase Hosting)
        │
        ▼
┌───────────────────┐
│   Welcome Screen  │  ← Suggested questions shown as chips
│   + Chat Input    │
└────────┬──────────┘
         │  User types question
         ▼
┌───────────────────────────────────────┐
│        React Frontend (Vite)          │
│  POST /api/chat  {message, session_id}│
└────────────────┬──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│       FastAPI Backend (Cloud Run)     │
│  chat_router → agent_service.run()   │
└────────────────┬──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│     Google ADK  LlmAgent              │
│  (Vertex AI Gemini 2.5 Flash)         │
│                                       │
│  Intent Detection                     │
│  ┌─────────────────────────────────┐  │
│  │ timeline?  → get_timeline()     │  │
│  │ step?      → explain_step()     │  │
│  │ doc query? → search_rag()       │  │
│  │ eligibility→ check_eligibility()│  │
│  │ faq?       → get_faq()          │  │
│  └─────────────────────────────────┘  │
└────────────────┬──────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────────────┐
│  Firestore   │  │  Vertex AI RAG Engine│
│  (sessions)  │  │  (ECI docs corpus)   │
└──────────────┘  └──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│       Agent assembles response        │
│       → streamed back to React UI     │
└───────────────────────────────────────┘
```

---

## 6. API Reference

| Method | Endpoint | Input | Output | Auth |
|---|---|---|---|---|
| `POST` | `/api/chat` | `{ message: str, session_id: str }` | `{ reply: str, sources: list, session_id: str }` | None (public) |
| `GET` | `/api/session/{session_id}` | session_id (path) | `{ history: list[message] }` | None |
| `DELETE` | `/api/session/{session_id}` | session_id (path) | `{ deleted: bool }` | None |
| `GET` | `/api/health` | — | `{ status: "ok" }` | None |
| `GET` | `/api/timeline` | `?type=general\|state` | `{ phases: list[phase] }` | None |

---

## 7. Code Structure

```
votesaathi/
│
├── frontend/                        # React + Vite app
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx       # Main chat thread display
│   │   │   ├── MessageBubble.jsx    # Individual message with source citations
│   │   │   ├── InputBar.jsx         # Text input + send button
│   │   │   ├── SuggestionChips.jsx  # Predefined question shortcuts
│   │   │   ├── TimelineView.jsx     # Visual election phase timeline
│   │   │   └── SourcePanel.jsx      # Shows RAG document sources
│   │   ├── hooks/
│   │   │   ├── useChat.js           # Chat state + API call logic
│   │   │   └── useSession.js        # Session ID management
│   │   ├── services/
│   │   │   └── api.js               # Axios wrapper for backend calls
│   │   ├── App.jsx                  # Root layout
│   │   └── main.jsx                 # Vite entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── backend/                         # FastAPI Python app
│   ├── main.py                      # FastAPI app init + router registration
│   ├── routers/
│   │   ├── chat.py                  # /api/chat and /api/session routes
│   │   ├── timeline.py              # /api/timeline route
│   │   └── health.py                # /api/health route
│   ├── agent/
│   │   ├── election_agent.py        # ADK LlmAgent definition + tool bindings
│   │   ├── tools/
│   │   │   ├── rag_search.py        # Calls Vertex AI RAG Engine
│   │   │   ├── get_timeline.py      # Returns election phase data
│   │   │   ├── explain_step.py      # Explains a specific election step
│   │   │   ├── check_eligibility.py # Voter eligibility logic
│   │   │   └── get_faq.py           # Returns structured FAQ answers
│   │   └── session_manager.py       # Reads/writes chat history to Firestore
│   ├── services/
│   │   ├── firestore_service.py     # Firestore read/write wrappers
│   │   ├── rag_service.py           # Vertex AI RAG Engine client
│   │   └── secret_manager.py        # Fetches secrets from GCP Secret Manager
│   ├── config.py                    # Env vars + GCP project config
│   ├── requirements.txt
│   └── Dockerfile
│
├── rag-corpus/                      # Offline: ECI document ingestion scripts
│   ├── ingest_docs.py               # Uploads PDFs to Cloud Storage + indexes to RAG
│   └── documents/                   # ECI PDFs, election manuals, voter guides
│
├── cloudbuild.yaml                  # Cloud Build CI/CD pipeline
└── README.md
```

---

## 8. Backend Function Map

### `routers/chat.py`

| Function | Route / Input | Output | Responsibility |
|---|---|---|---|
| `post_chat()` | `POST /api/chat` · `ChatRequest(message, session_id)` | `ChatResponse(reply, sources, session_id)` | Entry point — calls agent service, returns reply |
| `get_session()` | `GET /api/session/{session_id}` | `SessionResponse(history)` | Fetches full chat history from Firestore |
| `delete_session()` | `DELETE /api/session/{session_id}` | `{ deleted: bool }` | Clears session from Firestore |

### `agent/election_agent.py`

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `build_agent()` | — | `LlmAgent` instance | Instantiates ADK agent with all tools bound |
| `run_agent()` | `message: str, history: list` | `AgentResult(text, sources)` | Runs the agent turn with full conversation context |

### `agent/tools/rag_search.py`

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `search_election_docs()` | `query: str` | `list[RAGChunk(text, source_url)]` | Queries Vertex AI RAG Engine, returns top-k chunks |

### `agent/tools/get_timeline.py`

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `get_election_timeline()` | `election_type: str` | `list[Phase(name, description, duration)]` | Returns structured election phases for general or state elections |

### `agent/tools/explain_step.py`

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `explain_step()` | `step_name: str` | `StepExplanation(title, summary, details, links)` | Returns plain-language explanation of a specific election step |

### `agent/tools/check_eligibility.py`

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `check_voter_eligibility()` | `age: int, citizen: bool, constituency: str` | `EligibilityResult(eligible: bool, reason: str)` | Determines voter eligibility based on ECI rules |

### `services/firestore_service.py`

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `get_session_history()` | `session_id: str` | `list[Message]` | Reads conversation history from Firestore |
| `append_message()` | `session_id: str, message: Message` | `None` | Appends a new message turn to session document |
| `delete_session()` | `session_id: str` | `None` | Deletes session document from Firestore |

---

## 9. Frontend Function / Component Map

### Components

| Component | Props / State | Responsibility |
|---|---|---|
| `ChatWindow` | `messages[]`, `isLoading` | Renders the full message thread; auto-scrolls on new message |
| `MessageBubble` | `message{role, text, sources}` | Displays a single chat turn; renders source chips if sources exist |
| `InputBar` | `onSend(text)`, `disabled` | Text input field + send button; handles Enter key |
| `SuggestionChips` | `suggestions[]`, `onSelect(text)` | Renders pre-written question shortcuts shown on empty state |
| `TimelineView` | `phases[]` | Renders a visual step-by-step election phase timeline |
| `SourcePanel` | `sources[]` | Slide-in panel showing RAG document citations |

### Hooks

| Hook | State / Returns | Responsibility |
|---|---|---|
| `useChat()` | `messages`, `sendMessage(text)`, `isLoading`, `error` | Manages full chat state; calls `api.js` `postChat()`; appends messages |
| `useSession()` | `sessionId` | Generates or retrieves UUID session ID from localStorage |

### Services

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `postChat(message, sessionId)` | `string, string` | `{ reply, sources }` | POST to `/api/chat`; returns agent response |
| `getTimeline(type)` | `"general" \| "state"` | `phases[]` | GET `/api/timeline` for timeline data |

---

## 10. Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│                                                                  │
│   [SuggestionChips] ──onClick──► [InputBar]                      │
│                                       │                          │
│                                  useChat.sendMessage()           │
│                                       │                          │
│                                  api.postChat()                  │
└──────────────────────────────────────────────────────────────────┘
                                        │
                              HTTPS POST /api/chat
                                        │
┌──────────────────────────────────────────────────────────────────┐
│                     CLOUD RUN (FastAPI)                          │
│                                                                  │
│  chat_router.post_chat()                                         │
│       │                                                          │
│       ├──► session_manager.get_history(session_id)               │
│       │         └──► Firestore ──► returns history[]             │
│       │                                                          │
│       └──► agent_service.run_agent(message, history)             │
│                 │                                                │
│                 ▼                                                │
│         ┌─────────────────────────────────────┐                 │
│         │     ADK LlmAgent (Gemini 2.5 Flash) │                 │
│         │                                     │                 │
│         │  Tool Router                         │                 │
│         │  ├─► rag_search()                   │                 │
│         │  │     └──► Vertex AI RAG Engine    │                 │
│         │  │           └──► Cloud Storage     │                 │
│         │  │                 (ECI PDFs)        │                 │
│         │  ├─► get_timeline()                 │                 │
│         │  ├─► explain_step()                 │                 │
│         │  ├─► check_eligibility()            │                 │
│         │  └─► get_faq()                      │                 │
│         └─────────────────────────────────────┘                 │
│                 │                                                │
│       agent returns AgentResult(text, sources)                  │
│                 │                                                │
│       session_manager.append_message() ──► Firestore            │
│                 │                                                │
│       returns ChatResponse(reply, sources, session_id)          │
└──────────────────────────────────────────────────────────────────┘
                                        │
                              JSON response
                                        │
┌──────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│                                                                  │
│   useChat appends message ──► [ChatWindow] renders               │
│   sources present? ──► [SourcePanel] slides in                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 11. Implementation Plan

### Phase 1 — Foundation (Days 1–2)
- [ ] Create GCP project, enable APIs (Vertex AI, Firestore, Cloud Run, Secret Manager)
- [ ] Set up Cloud Storage bucket + upload ECI documents (PDFs)
- [ ] Index ECI documents into Vertex AI RAG Engine corpus
- [ ] Scaffold FastAPI backend with health route + config
- [ ] Scaffold React + Vite frontend with basic layout
- [ ] Set up Secret Manager with Gemini API key + service account

### Phase 2 — Agent Core (Days 3–4)
- [ ] Build ADK `LlmAgent` with Gemini 2.5 Flash in `election_agent.py`
- [ ] Implement `rag_search` tool wired to Vertex AI RAG Engine
- [ ] Implement `get_timeline`, `explain_step`, `get_faq` tools
- [ ] Implement `check_eligibility` tool with ECI eligibility logic
- [ ] Wire agent to FastAPI `/api/chat` route
- [ ] Implement Firestore session management (get, append, delete)

### Phase 3 — Frontend (Days 5–6)
- [ ] Build `ChatWindow`, `MessageBubble`, `InputBar` components
- [ ] Implement `useChat` and `useSession` hooks
- [ ] Add `SuggestionChips` with 6–8 seed questions
- [ ] Build `TimelineView` component for visual phase display
- [ ] Add `SourcePanel` for RAG citation display
- [ ] Wire frontend to backend API via `api.js`

### Phase 4 — Deploy & Polish (Day 7)
- [ ] Dockerize FastAPI backend
- [ ] Write `cloudbuild.yaml` for Cloud Build → Cloud Run deploy
- [ ] Deploy React frontend to Firebase Hosting
- [ ] CORS, env vars, health checks verified
- [ ] Accessibility pass (ARIA labels, keyboard nav, contrast)
- [ ] Write Pytest tests for all tools + routes
- [ ] Write Vitest tests for key React components
- [ ] Final README + demo prep

---

## 12. Tech Decisions & Rationale

| Decision | Choice | Rationale |
|---|---|---|
| **LLM** | Vertex AI Gemini 2.5 Flash | Low latency, cost-efficient, multimodal-ready, native GCP integration |
| **Agent Framework** | Google ADK (`LlmAgent`) | Native tool-calling, session-aware, designed for GCP; matches challenge intent |
| **RAG** | Vertex AI RAG Engine | Managed, serverless, integrates directly with Gemini — no custom vector DB needed |
| **Backend** | FastAPI (Python) | Async-ready, clean OpenAPI docs, lightweight, natural fit for ADK Python SDK |
| **Frontend** | React + Vite | Fast HMR, component-driven, wide ecosystem, handles streaming responses well |
| **Session Store** | Firestore | Serverless, real-time capable, native GCP, no infra to manage |
| **Backend Hosting** | Cloud Run | Serverless containers, scales to zero, cost-effective for hackathon workload |
| **Frontend Hosting** | Firebase Hosting | CDN-backed, GCP-native, one-command deploy, SSL out of the box |
| **Secrets** | Secret Manager | GCP best practice; no hardcoded API keys; integrates with Cloud Run env injection |
| **CI/CD** | Cloud Build | Native GCP pipeline; triggered on push to main; builds Docker image + deploys to Cloud Run |
| **Election Scope** | India (ECI) | Largest democracy; well-documented; strong public interest use case |
