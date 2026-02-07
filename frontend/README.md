# RAG Agent Frontend (Debugger)

A Streamlit-based dashboard for interacting with the RAG Agent. This interface acts as a full "debugger" to monitor the agent's internal processes.

## 🚀 Setup

1. **Start the Backend API**:
   ```bash
   python run.py
   ```

2. **Start the Frontend**:
   In a separate terminal:
   ```bash
   .\.venv\Scripts\python.exe -m streamlit run frontend/app.py
   ```

## 🛠️ Features

- **Chat & Persistence**: Full conversational history supported by PostgreSQL.
- **RAG Inspector**: Expandable sections show the exact document chunks retrieved from the knowledge base.
- **Latency Tracking**: Real-time response time monitoring for each agent interaction.
- **Knowledge Base Browser**: Sidebar list of all documents currently ingested.
- **Session Control**: Manually reset or clear `thread_id` to start fresh conversations.

## 🔌 Connection

The frontend connects to the FastAPI backend at `http://localhost:8000`. 
Environment override: `API_URL`.

## 🏗️ Structure

- `app.py`: Main UI and state handling.
- `api_client.py`: Decoupled HTTP client for backend communication.
