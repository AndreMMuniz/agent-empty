# How to Run the Frontend Dashboard

## Prerequisites

1. **Backend Running**: Ensure the backend API is running in one terminal:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Frontend Running**: Open a NEW terminal and run:
   ```bash
   streamlit run frontend/app.py
   ```

## Using the Dashboard

1. Open `http://localhost:8501` in your browser.
2. Check the sidebar for "API Connected ✅".
3. Start chatting!

## Troubleshooting

- **API Disconnected ❌**: Make sure the backend is running on port 8000.
- **Connection Refused**: Check if `API_URL` environment variable is set correctly (default: `http://localhost:8000`).
