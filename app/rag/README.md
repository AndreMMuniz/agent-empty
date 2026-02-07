# RAG Module Documentation

## Overview

This module implements the RAG (Retrieval-Augmented Generation) ingestion pipeline for the agent. It processes documents from the `data/raw` directory, chunks them, converts them to vector embeddings, and stores them in PostgreSQL with pgvector.

## Components

### 1. Configuration (`app/core/config.py`)

Centralized configuration management using Pydantic Settings. All RAG-related settings are defined here:

- **Embedding Configuration**: Model name and Ollama base URL
- **Vector Store Settings**: Collection name and vector dimensions
- **Chunking Parameters**: Chunk size and overlap
- **Data Paths**: Raw and processed data directories

### 2. Vector Store (`app/rag/store.py`)

Manages the connection to the PGVector store:

- **Singleton Pattern**: Ensures single vector store instance
- **Ollama Embeddings**: Configured embedding model
- **PGVector Integration**: LangChain PGVector with PostgreSQL
- **Error Handling**: Graceful connection failure handling

Key functions:
- `get_embeddings()`: Initialize Ollama embeddings
- `get_vector_store()`: Get or create vector store instance
- `reset_vector_store()`: Reset singleton for testing

### 3. Ingestion Pipeline (`app/rag/ingestion.py`)

Complete document processing pipeline:

**Supported File Types:**
- PDF (`.pdf`)
- Text (`.txt`)
- Images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`)

**Processing Steps:**
1. File discovery in `data/raw`
2. File type detection
3. Document loading (PDF/TXT/Image)
4. Text chunking with RecursiveCharacterTextSplitter
5. Metadata enrichment
6. Vector embedding generation
7. Storage in PGVector

**Key Classes:**
- `DocumentProcessor`: Main processing class
  - `discover_files()`: Find supported files
  - `process_file()`: Process single file
  - `ingest_directory()`: Batch process directory

**Main Function:**
- `ingest_documents(directory)`: Entry point for ingestion

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Database Configuration
DATABASE_URL=postgresql://agent_user:agent_password@localhost:5432/agent_db

# LLM Configuration
LLM_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434

# Embedding Configuration
EMBEDDING_MODEL=nomic-embed-text
VECTOR_DIMENSIONS=768

# Vector Store Configuration
VECTOR_COLLECTION_NAME=agent_documents

# Chunking Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Data Paths
RAW_DATA_PATH=data/raw
PROCESSED_DATA_PATH=data/processed
```

## Usage

### Prerequisites

1. **Start PostgreSQL with pgvector:**
   ```bash
   docker-compose up -d
   ```

2. **Start Ollama and pull the embedding model:**
   ```bash
   ollama pull nomic-embed-text
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Running Ingestion

**Method 1: Direct execution**
```bash
python -m app.rag.ingestion
```

**Method 2: From Python code**
```python
from app.rag.ingestion import ingest_documents

# Ingest from default directory (data/raw)
stats = ingest_documents()

# Ingest from custom directory
from pathlib import Path
stats = ingest_documents(Path("path/to/documents"))

print(f"Processed {stats['processed_files']} files")
print(f"Created {stats['total_chunks']} chunks")
```

### Testing

Three test scripts are provided:

1. **Test Configuration:**
   ```bash
   python test_rag_config.py
   ```
   Verifies all configuration values are loaded correctly.

2. **Test Vector Store:**
   ```bash
   python test_vector_store.py
   ```
   Tests embeddings initialization, vector store connection, and basic operations.

3. **Test Ingestion:**
   ```bash
   python test_ingestion.py
   ```
   Creates sample files, runs ingestion, and verifies results.

## Architecture

```
┌─────────────────┐
│   data/raw/     │
│  (PDF/TXT/IMG)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  DocumentProcessor      │
│  - File Discovery       │
│  - Type Detection       │
│  - Document Loading     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Text Chunking          │
│  RecursiveCharacter     │
│  TextSplitter           │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Ollama Embeddings      │
│  (nomic-embed-text)     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  PGVector Store         │
│  (PostgreSQL + pgvector)│
└─────────────────────────┘
```

## Troubleshooting

### Common Issues

**1. "Failed to initialize embeddings"**
- Ensure Ollama is running: `ollama serve`
- Pull the embedding model: `ollama pull nomic-embed-text`

**2. "Failed to initialize vector store"**
- Check PostgreSQL is running: `docker-compose ps`
- Verify DATABASE_URL in `.env`
- Check database logs: `docker-compose logs db`

**3. "No files found to process"**
- Verify files exist in `data/raw/`
- Check file extensions are supported
- Ensure RAW_DATA_PATH is correct in `.env`

**4. "Unsupported file type"**
- Only PDF, TXT, and common image formats are supported
- Check the `SUPPORTED_EXTENSIONS` dict in `ingestion.py`

## Database Schema

The PGVector extension creates these tables:

- `langchain_pg_collection`: Stores collection metadata
- `langchain_pg_embedding`: Stores vector embeddings and documents

You can inspect these using pgAdmin at http://localhost:5050:
- Email: admin@admin.com
- Password: admin

## Next Steps

After ingestion is complete, you can:

1. **Query the vector store:**
   ```python
   from app.rag.store import get_vector_store
   
   store = get_vector_store()
   results = store.similarity_search("your query", k=5)
   ```

2. **Integrate with your agent:**
   - Use the vector store for retrieval in your agent nodes
   - Implement RAG-based question answering
   - Add context from retrieved documents to LLM prompts

3. **Monitor and maintain:**
   - Regularly update documents in `data/raw/`
   - Re-run ingestion to update the vector store
   - Monitor chunk quality and adjust CHUNK_SIZE/CHUNK_OVERLAP
