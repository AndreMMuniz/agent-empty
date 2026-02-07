import json
import logging
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from app.core.config import settings

# Global Connection Pool
pool: AsyncConnectionPool = None

logger = logging.getLogger("uvicorn.error")

async def init_db():
    """Initializes the database connection pool and creates tables."""
    global pool
    try:
        pool = AsyncConnectionPool(conninfo=settings.DATABASE_URL, min_size=0, max_size=10, kwargs={"autocommit": True})
        await pool.open()
        logger.info("Database connection pool established.")
        
        # Create structured logging table if not exists
        await create_tables()
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise e

async def close_db():
    """Closes the database connection pool."""
    global pool
    if pool:
        await pool.close()
        logger.info("Database connection pool closed.")

async def create_tables():
    """Creates necessary tables for the application."""
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS logs_analysis (
                    id SERIAL PRIMARY KEY,
                    thread_id TEXT,
                    query TEXT,
                    result JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            logger.info("Table 'logs_analysis' checked/created.")

async def log_analysis(thread_id: str, query: str, result: dict | str):
    """
    Logs structured analysis results to the database.
    """
    if not pool:
        logger.warning("Database pool not initialized. Skipping log.")
        return

    try:
        # Ensure result is JSON serializable if it's a dict, otherwise treat as text
        if isinstance(result, dict):
            result_json = json.dumps(result)
        else:
            # Wrap text in a JSON structure for consistency
            result_json = json.dumps({"text": result})

        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO logs_analysis (thread_id, query, result) VALUES (%s, %s, %s)",
                    (thread_id, query, result_json)
                )
    except Exception as e:
        logger.error(f"Failed to log analysis: {e}")

def get_pool():
    """Returns the global connection pool."""
    return pool
