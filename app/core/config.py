from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://agent_user:agent_password@localhost:5432/agent_db"
    
    # LLM Configuration
    LLM_MODEL: str = "llama3.1:8b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = "nomic-embed-text"
    VECTOR_DIMENSIONS: int = 768
    
    # Vector Store Configuration
    VECTOR_COLLECTION_NAME: str = "agent_documents"
    
    # Chunking Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Data Paths
    RAW_DATA_PATH: str = "data/raw"
    PROCESSED_DATA_PATH: str = "data/processed"
    
    class Config:
        env_file = ".env"
        extra = "ignore"
    
    def get_raw_data_dir(self) -> Path:
        """Get the raw data directory as a Path object."""
        return Path(self.RAW_DATA_PATH)
    
    def get_processed_data_dir(self) -> Path:
        """Get the processed data directory as a Path object."""
        return Path(self.PROCESSED_DATA_PATH)

settings = Settings()
