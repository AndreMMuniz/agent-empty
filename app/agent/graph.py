from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from app.agent.state import AgentState
from app.agent.nodes import call_model, should_continue, tools

def create_graph(checkpointer=None):
    """
    Constructs the StateGraph for the tool-calling agent.
    
    Args:
        checkpointer: An initialized checkpointer instance (e.g., PostgresSaver).
    """
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools)) # Prebuilt ToolNode handles tool execution

    # Edges (Flow)
    workflow.add_edge(START, "agent")
    
    # Conditional Edge: Agent -> (Tools OR End)
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "__end__": END
        }
    )
    
    # If tool was used, loop back to agent to generate final response
    workflow.add_edge("tools", "agent")

    # Compile the graph
    return workflow.compile(checkpointer=checkpointer)
