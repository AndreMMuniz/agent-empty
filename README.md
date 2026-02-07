# Bubble.io Analysis & Consulting Agent (RAG Enabled)

An intelligent assistant built with **LangGraph**, **FastAPI**, and **PostgreSQL (PGVector)** to provide technical consulting and log analysis for Bubble.io developers. Now featuring a complete **RAG Engine** and an **Observability Dashboard**.

## 🚀 Overview

This project implements an AI agent capable of contextually switching between two operating modes:
1.  **Technical Consulting (RAG)**: Answers questions using a private knowledge base (PDFs, docs, manuals).
2.  **Log Analysis**: Processes errors, stack traces, and HTTP codes to diagnose issues and suggest fixes.

The system uses **persistent memory** via PostgreSQL, context isolation through **tool-calling orchestration**, and a robust **RAG (Retrieval-Augmented Generation)** pipeline.

## 🏗️ Architecture

The structure follows principles of modularity and separation of concerns:

```text
agent-empty/
├── app/
│   ├── core/               # Global settings, database, and telemetry
│   ├── agent/              # LangGraph logic (Nodes, State, Graph, Tools)
│   ├── rag/                # RAG ingestion pipeline and vector search
├── frontend/               # Streamlit Dashboard (API Client)
├── data/                   # Raw documents and evaluation datasets
├── docker-compose.yml      # Infrastructure (Postgres + PGVector + pgAdmin)
├── requirements.txt        # Project dependencies
└── run.py                  # Windows-compatible entrypoint
```

## 🛠️ Technologies

- **AI Orchestration**: LangGraph & LangChain (Agent-Tools flow)
- **Models**: Ollama (Llama 3.1 & Nomic Embed Text)
- **Database**: PostgreSQL with `PGVector` extension
- **Web API**: FastAPI
- **Frontend**: Streamlit
- **State Persistence**: `PostgresSaver` (LangGraph Checkpoint)
- **Observability**: `structlog` & Streamlit Debugger

## ⚙️ How to Run

### 1. Infrastructure
```bash
docker-compose up -d
```

### 2. Backend API
```bash
# Windows
python run.py
```

### 3. Frontend Dashboard
```bash
# In a new terminal
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

## 📚 RAG Ingestion

To feed the agent with your own documents:
1.  Place files (.pdf, .txt, .png, .jpg) in `data/raw/`.
2.  Run the ingestion pipeline:
    ```bash
    python -m app.rag.ingestion
    ```

## 🔌 API Endpoints

### `GET /files`
List all ingested documents.

### `POST /chat`
Payload: `{"message": "...", "thread_id": "..."}`
- **Response**: Enriched with `response`, `context` (retrieved chunks), and `latency`.

## 🔍 Observability (Debugger)

The **Frontend Dashboard** includes a real-time debugger:
- **Retrieved Context**: See exactly which document chunks were sent to the LLM.
- **Latency Monitoring**: Track response time in seconds.
- **File Inspector**: List all documents currently in the knowledge base.
- **pgAdmin**: Access `http://localhost:5050` to view history tables.

## 🗺️ Roadmap

- [x] Complete implementation of the RAG ingestion pipeline.
- [x] Integration of semantic search with PGVector.
- [x] Streamlit Frontend Dashboard.
- [x] Observability features (latency + retrieved context).
- [ ] Addition of evaluation metrics via LLM Judge (Planned).
- [ ] Support for multiple channels (WhatsApp/Telegram).

---
Developed by Andre Muniz
