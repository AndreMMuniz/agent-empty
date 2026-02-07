# Quick Setup Guide - RAG Engine Phase 2

This guide will help you get the RAG ingestion pipeline up and running.

## Prerequisites Checklist

- [ ] Docker installed and running
- [ ] Ollama installed and running
- [ ] Python 3.10+ with virtual environment

## Step-by-Step Setup

### 1. Start PostgreSQL with pgvector

```bash
# Start the database container
docker-compose up -d

# Verify it's running
docker-compose ps
```

You should see the `agent_db` container running.

### 2. Install Python Dependencies

```bash
# Activate your virtual environment (if not already active)
# On Windows:
.venv\Scripts\activate

# Install/update dependencies
pip install -r requirements.txt
```

### 3. Start Ollama and Pull Models

```bash
# Start Ollama (if not already running)
ollama serve

# In another terminal, pull the required models
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# The defaults should work, but you can edit .env if needed
```

### 5. Verify Installation

Run the three test scripts in order:

```bash
# Test 1: Configuration
python test_rag_config.py

# Test 2: Vector Store Connection
python test_vector_store.py

# Test 3: Full Ingestion Pipeline
python test_ingestion.py
```

If all tests pass, you're ready to go! ✅

## Using the RAG Engine

### Add Your Documents

Place your files in the `data/raw/` directory:

```bash
# Create the directory if it doesn't exist
mkdir -p data/raw

# Add your files (PDF, TXT, or images)
# Example:
# cp /path/to/your/document.pdf data/raw/
# cp /path/to/your/notes.txt data/raw/
```

### Run Ingestion

```bash
# Process all files in data/raw/
python -m app.rag.ingestion
```

You'll see output like:
```
=== Ingestion Statistics ===
Total files: 5
Processed: 5
Failed: 0
Total chunks: 127
```

### Query the Vector Store

```python
from app.rag.store import get_vector_store

# Get the vector store
store = get_vector_store()

# Search for relevant documents
results = store.similarity_search("your query here", k=5)

# Print results
for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(f"Content: {doc.page_content[:200]}...")
    print(f"Source: {doc.metadata['source_file']}")
```

## Troubleshooting

### "Failed to initialize embeddings"
- Make sure Ollama is running: `ollama serve`
- Pull the model: `ollama pull nomic-embed-text`

### "Failed to initialize vector store"
- Check PostgreSQL: `docker-compose ps`
- Check logs: `docker-compose logs db`
- Verify DATABASE_URL in `.env`

### "No files found to process"
- Verify files exist in `data/raw/`
- Check file extensions (.pdf, .txt, .png, .jpg, etc.)

## Next Steps

1. **Integrate with your agent**: Use the vector store for retrieval in your agent nodes
2. **Implement RAG**: Add retrieved context to your LLM prompts
3. **Monitor performance**: Adjust chunk size and overlap as needed

For detailed documentation, see: `app/rag/README.md`
