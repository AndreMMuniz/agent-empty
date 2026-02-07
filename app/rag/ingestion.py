"""
RAG Ingestion Pipeline Module

This module handles the complete document ingestion process:
1. Discovers files in the raw data directory
2. Detects file types (PDF, TXT, images)
3. Loads and processes documents
4. Chunks text into manageable pieces
5. Generates embeddings and stores in vector database
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import structlog
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredImageLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.core.config import settings
from app.rag.store import get_vector_store

logger = structlog.get_logger(__name__)


class DocumentProcessor:
    """Handles document processing and ingestion into the vector store."""
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        '.pdf': 'pdf',
        '.txt': 'text',
        '.png': 'image',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.gif': 'image',
        '.bmp': 'image',
    }
    
    def __init__(self):
        """Initialize the document processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        self.vector_store = None
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'total_chunks': 0,
        }
    
    def _get_file_type(self, file_path: Path) -> str:
        """
        Determine the file type based on extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type string ('pdf', 'text', 'image', or 'unknown')
        """
        extension = file_path.suffix.lower()
        return self.SUPPORTED_EXTENSIONS.get(extension, 'unknown')
    
    def _load_document(self, file_path: Path) -> List[Document]:
        """
        Load a document based on its file type.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of loaded documents
            
        Raises:
            ValueError: If file type is not supported
        """
        file_type = self._get_file_type(file_path)
        file_path_str = str(file_path)
        
        logger.info(
            "Loading document",
            file=file_path.name,
            type=file_type,
        )
        
        try:
            if file_type == 'pdf':
                loader = PyPDFLoader(file_path_str)
                return loader.load()
            
            elif file_type == 'text':
                loader = TextLoader(file_path_str, encoding='utf-8')
                return loader.load()
            
            elif file_type == 'image':
                loader = UnstructuredImageLoader(file_path_str)
                return loader.load()
            
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(
                "Failed to load document",
                file=file_path.name,
                error=str(e),
            )
            raise
    
    def _chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents
        """
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def _add_metadata(self, chunks: List[Document], file_path: Path) -> List[Document]:
        """
        Add metadata to document chunks.
        
        Args:
            chunks: List of document chunks
            file_path: Original file path
            
        Returns:
            Chunks with enhanced metadata
        """
        for chunk in chunks:
            chunk.metadata.update({
                'source_file': file_path.name,
                'file_type': self._get_file_type(file_path),
                'file_path': str(file_path),
            })
        return chunks
    
    def process_file(self, file_path: Path) -> bool:
        """
        Process a single file: load, chunk, and store.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Processing file", file=file_path.name)
            
            # Load the document
            documents = self._load_document(file_path)
            
            # Chunk the documents
            chunks = self._chunk_documents(documents)
            
            # Add metadata
            chunks = self._add_metadata(chunks, file_path)
            
            # Store in vector database
            if self.vector_store is None:
                self.vector_store = get_vector_store()
            
            # Extract texts and metadatas for batch insertion
            texts = [chunk.page_content for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            self.stats['processed_files'] += 1
            self.stats['total_chunks'] += len(chunks)
            
            logger.info(
                "File processed successfully",
                file=file_path.name,
                chunks=len(chunks),
            )
            return True
            
        except Exception as e:
            self.stats['failed_files'] += 1
            logger.error(
                "Failed to process file",
                file=file_path.name,
                error=str(e),
            )
            return False
    
    def discover_files(self, directory: Path) -> List[Path]:
        """
        Discover all supported files in a directory.
        
        Args:
            directory: Directory to search
            
        Returns:
            List of file paths
        """
        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return []
        
        files = []
        for ext in self.SUPPORTED_EXTENSIONS.keys():
            files.extend(directory.glob(f"*{ext}"))
        
        logger.info(f"Discovered {len(files)} files in {directory}")
        return files
    
    def ingest_directory(self, directory: Path = None) -> Dict[str, Any]:
        """
        Ingest all documents from a directory.
        
        Args:
            directory: Directory to ingest from (defaults to RAW_DATA_PATH)
            
        Returns:
            Dictionary with ingestion statistics
        """
        if directory is None:
            directory = settings.get_raw_data_dir()
        
        logger.info("Starting ingestion", directory=str(directory))
        
        # Discover files
        files = self.discover_files(directory)
        self.stats['total_files'] = len(files)
        
        if not files:
            logger.warning("No files found to process")
            return self.stats
        
        # Process each file
        for file_path in files:
            self.process_file(file_path)
        
        logger.info(
            "Ingestion complete",
            total_files=self.stats['total_files'],
            processed=self.stats['processed_files'],
            failed=self.stats['failed_files'],
            total_chunks=self.stats['total_chunks'],
        )
        
        return self.stats


def ingest_documents(directory: Path = None) -> Dict[str, Any]:
    """
    Main entry point for document ingestion.
    
    Args:
        directory: Directory to ingest from (defaults to RAW_DATA_PATH)
        
    Returns:
        Dictionary with ingestion statistics
    """
    processor = DocumentProcessor()
    return processor.ingest_directory(directory)


if __name__ == "__main__":
    # Allow running this module directly for testing
    import sys
    
    if len(sys.argv) > 1:
        custom_dir = Path(sys.argv[1])
        stats = ingest_documents(custom_dir)
    else:
        stats = ingest_documents()
    
    print("\n=== Ingestion Statistics ===")
    print(f"Total files: {stats['total_files']}")
    print(f"Processed: {stats['processed_files']}")
    print(f"Failed: {stats['failed_files']}")
    print(f"Total chunks: {stats['total_chunks']}")
