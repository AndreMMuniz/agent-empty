import sys
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import os

# Windows compatibility for psycopg
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.agent.graph import create_graph
from app.core.database import init_db, close_db, get_pool, log_analysis

# Global graph instance (set on startup)
agent_runnable = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    1. Initialize Database Pool
    2. Setup Checkpointer with the pool
    3. Compile Graph with Checkpointer
    """
    # Startup
    await init_db()
    pool = get_pool()
    
    # Initialize Checkpointer with the shared pool
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup() # Ensure tables exist
    
    global agent_runnable
    agent_runnable = create_graph(checkpointer=checkpointer)
    
    yield
    
    # Shutdown
    await close_db()

app = FastAPI(
    title="LangGraph Agent API",
    description="API for querying the Bubble.io Consultant Agent",
    version="1.0.0",
    lifespan=lifespan
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None
    sources: list[str] = []  # New field for fonts

import time
from pathlib import Path
from typing import List, Optional

class ChatResponse(BaseModel):
    response: str
    thread_id: str | None = None
    context: List[str] = [] # Retrieved documents content
    latency: float = 0.0     # Response time in seconds

@app.get("/")
async def root():
    return {"status": "ok", "message": "Agent API is running with Lifecycle Management"}

@app.get("/files")
async def list_files():
    """List all available files in the raw data directory."""
    try:
        raw_path = Path("data/raw")
        if not raw_path.exists():
            return {"files": []}
        files = [f.name for f in raw_path.iterdir() if f.is_file()]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message through the LangGraph agent.
    """
    if not agent_runnable:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        start_time = time.perf_counter()
        
        # Prepare input for the graph
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # Configuration for thread-based persistence
        config = {"configurable": {"thread_id": request.thread_id}} if request.thread_id else {}
        
        # Invoke the graph (async)
        result = await agent_runnable.ainvoke(inputs, config=config)
        
        end_time = time.perf_counter()
        latency = round(end_time - start_time, 2)
        
        # Extract the last message content (Agent response)
        last_message = result["messages"][-1]
        response_content = last_message.content
        
        # Extract context from ToolMessages
        context = []
        for msg in result["messages"]:
            if msg.type == "tool":
                # This message contains the output from the tool (RAG search results)
                context.append(str(msg.content))
        
        # STRUCTURED LOGGING (Side Effect)
        if request.thread_id:
            log_data = {
                "response": response_content,
                "latency": latency,
                "context_length": len(context)
            }
            await log_analysis(
                thread_id=request.thread_id, 
                query=request.message, 
                result=log_data
            )
        
        return ChatResponse(
            response=response_content,
            thread_id=request.thread_id,
            context=context,
            latency=latency
        )
            
    except Exception as e:
        # Log the error potentially too
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
