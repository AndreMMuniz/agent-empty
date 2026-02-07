from typing import Literal
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.agent.state import AgentState
from app.agent.utils import get_model

# Initialize model
model = get_model() # This is the full ChatOllama model

# Prompts
ROUTER_SYSTEM_PROMPT = """You are an intelligent router. 
Your goal is to classify the user's input into one of two categories: 'log_analysis' or 'consultation'.

- 'log_analysis': The user is providing error logs, stack traces, HTTP status codes (4xx, 5xx), or asking debugging questions related to specific errors.
- 'consultation': The user is asking general questions about Bubble.io, how to do something, best practices, or design advice.

Output ONLY the category name. Do not explain."""

CONSULTANT_SYSTEM_PROMPT = """You are a technical consultant specializing in bubble.io.

You have access to the tool's documentation.
You are able to provide advice and answer developer questions about how things work.
You analyze logs and, based on what you receive, provide information that can help resolve relevant problems with the bubble tool.
You receive feedback from users on whether your solution was effective and helped solve that problem.
You should learn from user feedback, whether negative or positive."""

ANALYST_SYSTEM_PROMPT = """You are a Log Analyst specializing in debugging web applications.
Your goal is to analyze error logs, identify root causes, and suggest fixes.
Be precise and technical. Focus on HTTP status codes, stack traces, and database errors."""

def get_messages_with_system(messages: list, system_prompt: str) -> list:
    """
    Filters out any existing SystemMessages from the history and 
    prepends the new, current SystemMessage.
    This prevents context pollution and "phantom" instructions.
    """
    # Filter out old SystemMessages
    clean_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
    # Prepend new SystemMessage
    return [SystemMessage(content=system_prompt)] + clean_messages

def router_node(state: AgentState):
    """
    Decides the next step based on user input.
    """
    messages = state["messages"]
    last_message = messages[-1].content if messages else "No input"
    
    # Simple prompt for classification
    router_messages = [
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=last_message)
    ]
    
    response = model.invoke(router_messages)
    decision = response.content.strip().lower()
    
    # Normalize decision
    intent = "consultation" # Default
    if "log" in decision or "analysis" in decision:
        intent = "log_analysis"
    
    # Update state with intent
    return {"intent": intent}

def consultant_node(state: AgentState):
    """
    Expert node for general consultation.
    """
    relevant_messages = get_messages_with_system(state["messages"], CONSULTANT_SYSTEM_PROMPT)
    # Note: We filter out system messages, but keep the history. 
    response = model.invoke(relevant_messages)
    return {"messages": [response]}

def analyst_node(state: AgentState):
    """
    Expert node for log analysis.
    """
    relevant_messages = get_messages_with_system(state["messages"], ANALYST_SYSTEM_PROMPT)
    response = model.invoke(relevant_messages)
    return {"messages": [response]}
