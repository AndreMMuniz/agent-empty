from typing import Literal
from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes.base import router_node, consultant_node, analyst_node

def route_decision(state: AgentState) -> Literal["analyst", "consultant"]:
    """
    Conditional edge function that reads the 'intent' from state 
    and returns the name of the next node.
    """
    intent = state.get("intent", "consultation")
    if intent == "log_analysis":
        return "analyst"
    return "consultant"

def create_graph(checkpointer=None):
    """
    Constructs the StateGraph for the agent with routing.
    
    Args:
        checkpointer: An initialized checkpointer instance (e.g., PostgresSaver).
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("consultant", consultant_node)
    workflow.add_node("analyst", analyst_node)

    # Add edges
    # START -> Router -> (Decision) -> Expert -> END
    workflow.add_edge(START, "router")
    
    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "analyst": "analyst",
            "consultant": "consultant"
        }
    )
    
    workflow.add_edge("analyst", END)
    workflow.add_edge("consultant", END)

    # Compile the graph
    return workflow.compile(checkpointer=checkpointer)
