from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://agent_user:agent_password@localhost:5432/agent_db"
    LLM_MODEL: str = "llama3.1:8b"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
