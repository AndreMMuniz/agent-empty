# RAG Agent Frontend

A Streamlit-based dashboard for interacting with the RAG Agent. It connects to the backend API via HTTP requests.

## Setup

1. **Start the Backend API**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Start the Frontend**:
   In a separate terminal:
   ```bash
   streamlit run frontend/app.py
   ```

## Configuration

The frontend connects to `http://localhost:8000` by default. You can change this by setting the `API_URL` environment variable.

## Features

- **Chat Interface**: Ask questions and get answers.
- **Session Management**: Each session has a unique ID (`thread_id`) stored in `st.session_state`.
- **API Health Check**: Visual indicator in the sidebar showing if the backend is reachable.
- **Clear History**: Button to restart the conversation.

## Architecture

- `app.py`: Main Streamlit application logic and UI.
- `api_client.py`: Wrapper for backend API calls (`requests` library).
