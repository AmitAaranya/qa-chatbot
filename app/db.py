import chromadb
from chromadb.errors import NotFoundError
from typing import List, Optional
import uuid

class ChromaDBManager:
    def __init__(self, collection_name: str = "qa_collection"):

        self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection(collection_name)
        except NotFoundError:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )

    def add_documents(self, documents: List[str], metadatas: Optional[List[dict]] = None) -> List[str]:
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
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=['documents', 'distances', 'metadatas']
        )
        
        return results
