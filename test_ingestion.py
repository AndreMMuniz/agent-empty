"""
Test script to verify the ingestion pipeline.

This script will:
1. Create sample test files in data/raw
2. Run the ingestion pipeline
3. Verify the results in the vector store

Prerequisites:
1. Docker containers must be running (docker-compose up -d)
2. Ollama must be running with the embedding model pulled
3. .env file must be configured
"""

from pathlib import Path
from app.rag.ingestion import ingest_documents
from app.rag.store import get_vector_store
from app.core.config import settings

def create_sample_files():
    """Create sample test files for ingestion."""
    print("=== Creating Sample Files ===")
    
    raw_dir = settings.get_raw_data_dir()
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a sample TXT file
    txt_file = raw_dir / "sample.txt"
    txt_content = """
    This is a sample text document for testing the RAG ingestion pipeline.
    
    It contains multiple paragraphs to test the chunking functionality.
    The text splitter should break this into appropriate chunks based on
    the configured chunk size and overlap settings.
    
    This is important for ensuring that the retrieval system can find
    relevant information efficiently when users ask questions.
    """
    txt_file.write_text(txt_content.strip())
    print(f"✅ Created: {txt_file}")
    
    # Create another sample TXT file
    txt_file2 = raw_dir / "sample2.txt"
    txt_content2 = """
    This is a second sample document about a different topic.
    
    It discusses the importance of vector embeddings in modern AI systems.
    Vector embeddings allow us to represent text as numerical vectors,
    which can then be compared using similarity metrics.
    
    This enables semantic search capabilities that go beyond simple
    keyword matching.
    """
    txt_file2.write_text(txt_content2.strip())
    print(f"✅ Created: {txt_file2}")
    
    print(f"\nSample files created in: {raw_dir}")
    return raw_dir

def test_ingestion():
    """Test the ingestion pipeline."""
    print("\n=== Testing Ingestion Pipeline ===")
    
    try:
        # Run ingestion
        stats = ingest_documents()
        
        print("\n=== Ingestion Statistics ===")
        print(f"Total files: {stats['total_files']}")
        print(f"Processed: {stats['processed_files']}")
        print(f"Failed: {stats['failed_files']}")
        print(f"Total chunks: {stats['total_chunks']}")
        
        if stats['processed_files'] > 0:
            print("\n✅ Ingestion completed successfully!")
            return True
        else:
            print("\n⚠️  No files were processed")
            return False
            
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_storage():
    """Verify that documents were stored in the vector database."""
    print("\n=== Verifying Storage ===")
    
    try:
        store = get_vector_store()
        
        # Search for content from our sample files
        test_queries = [
            "RAG ingestion pipeline",
            "vector embeddings",
            "semantic search",
        ]
        
        for query in test_queries:
            print(f"\nSearching for: '{query}'")
            results = store.similarity_search(query, k=2)
            
            if results:
                print(f"✅ Found {len(results)} results")
                for i, doc in enumerate(results, 1):
                    print(f"\n  Result {i}:")
                    print(f"    Content: {doc.page_content[:100]}...")
                    print(f"    Source: {doc.metadata.get('source_file', 'unknown')}")
            else:
                print(f"⚠️  No results found")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the complete ingestion test."""
    print("=" * 60)
    print("RAG Ingestion Pipeline Test")
    print("=" * 60)
    print()
    
    # Create sample files
    raw_dir = create_sample_files()
    
    # Run ingestion
    ingestion_ok = test_ingestion()
    
    if not ingestion_ok:
        print("\n⚠️  Ingestion failed. Check the logs above for details.")
        return
    
    # Verify storage
    verification_ok = verify_storage()
    
    if verification_ok:
        print("\n" + "=" * 60)
        print("✅ All ingestion tests passed!")
        print("=" * 60)
        print(f"\nYou can now add your own files to: {raw_dir}")
        print("Then run: python -m app.rag.ingestion")
    else:
        print("\n⚠️  Verification failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
