import chromadb
from chromadb.errors import NotFoundError
from typing import List, Optional
import uuid

class ChromaDBManager:
    """A class to manage ChromaDB vector database operations for document storage and retrieval.
    
    This class provides an interface to store documents and perform similarity-based queries
    using ChromaDB's vector database capabilities.
    """
    
    def __init__(self, collection_name: str = "qa_collection"):
        """Initialize a ChromaDB collection.
        
        Args:
            collection_name (str, optional): Name of the collection to use. Defaults to "qa_collection".
        """
        self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection(collection_name)
        except NotFoundError:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )

    def add_documents(self, documents: List[str], metadatas: Optional[List[dict]] = None) -> List[str]:
        """Add documents to the ChromaDB collection.
        
        Args:
            documents (List[str]): List of document texts to add to the collection.
            metadata_list (Optional[List[dict]], optional): List of metadata dictionaries for each document. 
                Defaults to None.
        
        Returns:
            List[str]: List of generated UUIDs for the added documents.
        """
        ids = [str(uuid.uuid4()) for _ in documents]
        
        if metadatas is None:
            metadatas:list[dict] = [{} for _ in documents]
        
        # Add documents to collection
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        
        return ids

    def query_documents(self, query_text: str, n_results: int = 5) -> dict:
        """Query the collection for documents similar to the given text.
        
        Args:
            query_text (str): The text to use for similarity search.
            n_results (int, optional): Maximum number of results to return. Defaults to 5.
        
        Returns:
            dict: Query results containing 'documents', 'distances', and 'metadatas' keys.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=['documents', 'distances', 'metadatas']
        )
        
        return results
