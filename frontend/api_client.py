import requests
import os
from typing import Dict, Any, Optional
import time

class APIClient:
    """
    Client for interacting with the Agent API.
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:8000")
        
    def check_health(self) -> bool:
        """Check if the API is running."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=2)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def send_message(self, message: str, thread_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat message to the agent.
        
        Args:
            message: The user's query
            thread_id: Optional session ID for conversation history
            
        Returns:
            Dict containing the response and thread_id
        """
        payload = {"message": message}
        if thread_id:
            payload["thread_id"] = thread_id
            
        try:
            response = requests.post(f"{self.base_url}/chat", json=payload, timeout=60) # Increased timeout for RAG
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "response": "Error communicating with the agent."}
