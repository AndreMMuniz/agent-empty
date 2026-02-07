# Bubble.io Analysis & Consulting Agent

An intelligent assistant built with **LangGraph**, **FastAPI**, and **PostgreSQL (PGVector)** to provide technical consulting and log analysis for Bubble.io developers.

## 🚀 Overview

This project implements an AI agent capable of contextually switching between two operating modes:
1.  **Technical Consulting**: Answers questions about best practices, workflows, and design in Bubble.io.
2.  **Log Analysis**: Processes errors, stack traces, and HTTP codes to diagnose issues and suggest fixes.

The system uses **persistent memory** via PostgreSQL, context isolation through an **intelligent router**, and is prepared for **RAG (Retrieval-Augmented Generation)** with vector support.

## 🏗️ Architecture (Clean Architecture)

The structure follows principles of single responsibility and separation of concerns:

```text
agent-empty/
├── app/
│   ├── core/               # Global settings and database
│   ├── agent/              # LangGraph logic (Nodes, State, Graph)
│   ├── rag/                # RAG ingestion pipeline and vector search
│   └── evaluation/         # Quality evaluation (LLM Judge)
├── data/                   # Raw files and test datasets
├── docker-compose.yml      # Infrastructure (Postgres + PGVector + pgAdmin)
├── requirements.txt        # Project dependencies
└── run.py                  # Windows-compatible entrypoint
```

## 🛠️ Technologies

- **Language**: Python 3.12+
- **Web Framework**: FastAPI
- **AI Orchestration**: LangGraph & LangChain
- **Database**: PostgreSQL with `PGVector` extension
- **State Persistence**: `PostgresSaver` (LangGraph Checkpoint)
- **Containerization**: Docker & Docker Compose

## ⚙️ Environment Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.12 or higher
- Ollama instance (or API key for other models)

### Step-by-Step

1.  **Clone the repository**:
    ```bash
    git clone <your-repository>
    cd agent-empty
    ```

2.  **Configure environment variables**:
    Copy the example file to `.env` and adjust as needed:
    ```bash
    cp .env.example .env
    ```

3.  **Start infrastructure**:
    ```bash
    docker-compose up -d
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application**:
    ```bash
    python run.py
    ```

## 🔌 API Endpoints

### `GET /`
Checks if the API is online and connected to the database.

### `POST /chat`
Sends a message to the agent.

**Payload:**
```json
{
  "message": "How do I configure a Repeating Group?",
  "thread_id": "user-123"
}
```

**Response:**
- The agent generates a contextually isolated response.
- History is automatically saved in the database, allowing conversation resumption using the same `thread_id`.

## 🔍 Observability and Debug

- **pgAdmin**: Access `http://localhost:5050` (admin@admin.com / admin) to view history tables and analysis logs.
- **Structured Logs**: The project uses `structlog` for JSON-formatted logs, facilitating ingestion by monitoring tools.

## 🗺️ Roadmap

- [ ] Complete implementation of the RAG ingestion pipeline (PDF/CSV).
- [ ] Integration of semantic search with PGVector.
- [ ] Addition of evaluation metrics via LLM Judge.
- [ ] Support for multiple channels (WhatsApp/Telegram).

---
Developed by [Your Name/Company]
