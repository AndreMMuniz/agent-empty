"""
Test script to verify RAG configuration is loaded correctly.
"""

from app.core.config import settings

def test_config():
    """Test that all RAG configuration values are loaded."""
    print("=== RAG Configuration Test ===\n")
    
    print("Database Configuration:")
    print(f"  DATABASE_URL: {settings.DATABASE_URL}")
    
    print("\nLLM Configuration:")
    print(f"  LLM_MODEL: {settings.LLM_MODEL}")
    print(f"  OLLAMA_BASE_URL: {settings.OLLAMA_BASE_URL}")
    
    print("\nEmbedding Configuration:")
    print(f"  EMBEDDING_MODEL: {settings.EMBEDDING_MODEL}")
    print(f"  VECTOR_DIMENSIONS: {settings.VECTOR_DIMENSIONS}")
    
    print("\nVector Store Configuration:")
    print(f"  VECTOR_COLLECTION_NAME: {settings.VECTOR_COLLECTION_NAME}")
    
    print("\nChunking Configuration:")
    print(f"  CHUNK_SIZE: {settings.CHUNK_SIZE}")
    print(f"  CHUNK_OVERLAP: {settings.CHUNK_OVERLAP}")
    
    print("\nData Paths:")
    print(f"  RAW_DATA_PATH: {settings.RAW_DATA_PATH}")
    print(f"  PROCESSED_DATA_PATH: {settings.PROCESSED_DATA_PATH}")
    print(f"  Raw data directory: {settings.get_raw_data_dir()}")
    print(f"  Processed data directory: {settings.get_processed_data_dir()}")
    
    print("\n✅ Configuration loaded successfully!")

if __name__ == "__main__":
    test_config()
