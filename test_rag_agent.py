from app.agent.graph import create_graph
import structlog
from langchain_core.messages import HumanMessage

# Configure basic logging to see tool usage
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

def test_agent():
    print("Initializing Agent with RAG Tools...")
    graph = create_graph()
    
    print("\n=== Test 1: General Question (No Tool Expected) ===")
    response = graph.invoke({"messages": [HumanMessage(content="Hello, who are you?")]})
    print(f"Agent: {response['messages'][-1].content}")
    
    print("\n=== Test 2: RAG Question (Tool Expected) ===")
    query = "Summarize the content of sample.txt file."
    print(f"User: {query}")
    
    # Stream the execution to see steps
    for event in graph.stream({"messages": [HumanMessage(content=query)]}):
        for key, value in event.items():
            print(f"\n--- Node: {key} ---")
            if key == "tools":
                # Show tool output
                for msg in value["messages"]:
                    print(f"Tool Output: {msg.content[:200]}...") # Truncate for readability
            elif key == "agent":
                # Show agent response
                last_msg = value["messages"][-1]
                if last_msg.content:
                    print(f"Agent Response: {last_msg.content}")
                if last_msg.tool_calls:
                    print(f"Tool Call: {last_msg.tool_calls[0]['name']}")

if __name__ == "__main__":
    test_agent()
