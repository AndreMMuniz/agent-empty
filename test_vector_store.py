"""
Test script to verify vector store connection.

Prerequisites:
1. Docker containers must be running (docker-compose up -d)
2. Ollama must be running with the embedding model pulled
3. .env file must be configured
"""

import asyncio
from app.rag.store import get_vector_store, get_embeddings

def test_embeddings():
    """Test that embeddings can be initialized."""
    print("=== Testing Embeddings ===")
    try:
        embeddings = get_embeddings()
        print(f"✅ Embeddings initialized: {embeddings}")
        
        # Test embedding a simple text
        print("\nTesting embedding generation...")
        test_text = "This is a test sentence for embedding."
        embedding = embeddings.embed_query(test_text)
        print(f"✅ Generated embedding with dimension: {len(embedding)}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize embeddings: {e}")
        return False

def test_vector_store():
    """Test that vector store can be initialized."""
    print("\n=== Testing Vector Store ===")
    try:
        store = get_vector_store()
        print(f"✅ Vector store initialized: {store}")
        
        # Test adding a simple document
        print("\nTesting document addition...")
        test_docs = ["This is a test document."]
        test_metadata = [{"source": "test", "type": "test"}]
        
        ids = store.add_texts(texts=test_docs, metadatas=test_metadata)
        print(f"✅ Added test document with ID: {ids}")
        
        # Test similarity search
        print("\nTesting similarity search...")
        results = store.similarity_search("test document", k=1)
        print(f"✅ Found {len(results)} similar documents")
        if results:
            print(f"   Content: {results[0].page_content}")
            print(f"   Metadata: {results[0].metadata}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize vector store: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("RAG Vector Store Connection Test")
    print("=" * 50)
    print()
    
    # Test embeddings first
    embeddings_ok = test_embeddings()
    
    if not embeddings_ok:
        print("\n⚠️  Embeddings test failed. Make sure Ollama is running.")
        print("   Run: ollama pull nomic-embed-text")
        return
    
    # Test vector store
    store_ok = test_vector_store()
    
    if not store_ok:
        print("\n⚠️  Vector store test failed. Make sure PostgreSQL is running.")
        print("   Run: docker-compose up -d")
        return
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
