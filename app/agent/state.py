from typing import Annotated, TypedDict, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Standard state for the conversational agent.
    
    Attributes:
        messages: A list of messages (Human, AI, System) representing the conversation history.
        intent: The classified intent of the user (e.g., 'consultation', 'log_analysis').
    """
    messages: Annotated[list[BaseMessage], add_messages]
    intent: str | None
