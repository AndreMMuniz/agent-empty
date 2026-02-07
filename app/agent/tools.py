from langchain_core.tools import tool
from app.rag.store import get_vector_store
import structlog

logger = structlog.get_logger(__name__)

@tool
def search_knowledge_base(query: str) -> str:
    """
    Use this tool to search for technical information, logs, or documentation 
    in the knowledge base (vector store).
    Useful when the question is about specific processes, errors, or manuals.
    """
    try:
        logger.info("Searching knowledge base", query=query)
        vector_store = get_vector_store()
        
        # Search for the 3 most relevant chunks
        results = vector_store.similarity_search(query, k=3)
        
        if not results:
            logger.info("No results found", query=query)
            return "No relevant information found in the knowledge base."
            
        # Format the output for the Agent to read
        context = "\n\n".join([
            f"Source: {doc.metadata.get('source_file', 'unknown')}\nContent: {doc.page_content}" 
            for doc in results
        ])
        
        logger.info("Search successful", results=len(results))
        return context
        
    except Exception as e:
        logger.error("Search failed", error=str(e))
        return f"Error searching knowledge base: {str(e)}"
