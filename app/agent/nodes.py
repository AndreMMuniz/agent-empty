import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from app.agent.state import AgentState
from app.agent.tools import search_knowledge_base
from app.core.config import settings
import structlog

logger = structlog.get_logger(__name__)

# Initialize model with tools
# We use the model defined in config, ensuring it supports tool calling
# Llama 3.1 supports tool calling natively
tools = [search_knowledge_base]

# Initialize the model with the configuration
# bind_tools tells the model which tools are available
model = ChatOllama(
    model=settings.LLM_MODEL, 
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
).bind_tools(tools)

def call_model(state: AgentState, config: RunnableConfig):
    """
    Main node that calls the LLM.
    """
    messages = state["messages"]
    
    # System Prompt to define the persona and tool usage
    # We only add the system message if it's not already there (or as the first message)
    # This logic checks if the first message is a SystemMessage, if not prepends one.
    
    system_prompt = """You are an Expert Consultant Agent.
    
    Your goal is to help the user with technical questions, log analysis, and documentation.
    
    CRITICAL INSTRUCTIONS:
    1. Whenever the user asks a technical question or about a specific process/error, YOU MUST USE the 'search_knowledge_base' tool.
    2. Do not invent information. If the tool returns no results, state that you don't know based on the available knowledge.
    3. Be concise and professional.
    """
    
    if not messages or not isinstance(messages[0], SystemMessage):
        sys_msg = SystemMessage(content=system_prompt)
        messages = [sys_msg] + messages
    
    logger.info("Calling model", model=settings.LLM_MODEL)
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """
    Decides whether the agent should stop (respond) or search more data (tool call).
    """
    last_message = state["messages"][-1]
    
    # If the LLM requested a tool call, proceed to 'tools' node
    if last_message.tool_calls:
        logger.info("Model requested tool execution", tools=len(last_message.tool_calls))
        return "tools"
    
    # Otherwise, end execution
    logger.info("Model finished generation")
    return "__end__"
