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

    def get_files(self) -> List[str]:
        """Fetch list of available files from the backend."""
        try:
            response = requests.get(f"{self.base_url}/files", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return data.get("files", [])
            return []
        except requests.RequestException:
            return []

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
            # Increased timeout significantly for RAG + LLM generation
            response = requests.post(f"{self.base_url}/chat", json=payload, timeout=120) 
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "response": "Error communicating with the agent."}
