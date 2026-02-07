import asyncio
from langchain_core.messages import HumanMessage
from app.agent.nodes import router_node, consultant_node, analyst_node
from app.agent.state import AgentState

def test_router():
    print("Testing Router Logic...")
    
    # Test 1: Log Analysis
    state_log = {"messages": [HumanMessage(content="Error 500: Internal Server Error\nStack trace: ...")]}
    result_log = router_node(state_log)
    print(f"Input: Error log -> Intent: {result_log.get('intent')}")
    assert result_log.get("intent") == "log_analysis"
    
    # Test 2: Consultation
    state_chat = {"messages": [HumanMessage(content="How do I use backend workflows?")]}
    result_chat = router_node(state_chat)
    print(f"Input: Question -> Intent: {result_chat.get('intent')}")
    assert result_chat.get("intent") == "consultation"
    
    print("\nSUCCESS: Router classifies correctly.")

if __name__ == "__main__":
    test_router()
