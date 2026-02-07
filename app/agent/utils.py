import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_model():
    """
    Initializes and returns the ChatOllama model with the specified configuration.
    
    The model name is flexible and can be adjusted based on available local models.
    Defaulting to 'llama3.1:8b' as a robust local option, or 'llama4.1:8b' if specified by user.
    """
    # Using the model name specified by the user or a standard default
    # Note: 'llama4.1:8b' was requested, ensuring we try to use it.
    model_name = os.getenv("OLLAMA_MODEL", "llama4.1:8b") 
    
    return ChatOllama(
        model=model_name,
        temperature=0,  # Deterministic output
    )
