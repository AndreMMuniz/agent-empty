"""
RAG Vector Store Connection Module

This module manages the connection to the PGVector store for document embeddings.
It provides a singleton instance of the vector store configured with Ollama embeddings.
"""

from typing import Optional
from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings
from app.core.config import settings
import structlog

logger = structlog.get_logger(__name__)

# Global vector store instance (singleton pattern)
_vector_store: Optional[PGVector] = None


def get_embeddings() -> OllamaEmbeddings:
    """
    Initialize and return Ollama embeddings.
    
    Returns:
        OllamaEmbeddings: Configured embedding model
    """
    return OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )


def get_vector_store() -> PGVector:
    """
    Get or create the PGVector store instance.
    
    This function implements a singleton pattern to ensure only one
    vector store connection is maintained throughout the application.
    
    Returns:
        PGVector: Configured vector store instance
        
    Raises:
        Exception: If connection to the database fails
    """
    global _vector_store
    
    if _vector_store is not None:
        return _vector_store
    
    try:
        logger.info(
            "Initializing vector store",
            collection_name=settings.VECTOR_COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL,
        )
        
        embeddings = get_embeddings()
        
        # Initialize PGVector with the new langchain-postgres syntax
        _vector_store = PGVector(
            embeddings=embeddings,
            collection_name=settings.VECTOR_COLLECTION_NAME,
            connection=settings.DATABASE_URL,
            use_jsonb=True,
        )
        
        logger.info("Vector store initialized successfully")
        return _vector_store
        
    except Exception as e:
        logger.error("Failed to initialize vector store", error=str(e))
        raise


def reset_vector_store() -> None:
    """
    Reset the vector store singleton.
    
    This is useful for testing or when you need to reinitialize
    the connection with different settings.
    """
    global _vector_store
    _vector_store = None
    logger.info("Vector store reset")
