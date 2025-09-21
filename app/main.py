import uuid
from typing import Any
import pandas as pd
from .llm import GoogleGeminiLLM
from .prompt import QA_SYSTEM_PROMPT, create_user_prompt
from .db import ChromaDBManager


class Chat:
    """A chat interface that combines LLM capabilities with vector database search.
    
    This class manages the conversation flow, storing chat history, and retrieving
    relevant context from a vector database to provide informed responses.
    """
    
    def __init__(self):
        """Initialize a new chat session with LLM and vector database components."""
        self.message_store = []
        self.ai = GoogleGeminiLLM(system_prompt=QA_SYSTEM_PROMPT)
        self.db = ChromaDBManager(collection_name=str(uuid.uuid4()))

    
    def __call__(self, user_message) -> Any:
        """Process user message and generate a response using context from the database.
        
        Args:
            user_message: The message from the user to process.
            
        Yields:
            str: Generated response chunks from the LLM.
        """
        context = self.__create_context(self.db.query_documents(user_message))
        user_prompt = create_user_prompt(context, user_message)
        self.message_store.append(self.ai.format_prompts(user_prompt, role="user"))
        response = ""
        for chunk in self.ai.generate_text(self.message_store):
            if isinstance(chunk, str):
                response += chunk
                yield chunk
        self.message_store.pop()  # Remove the last user message
        self.message_store.append(self.ai.format_prompts(user_message, role="user"))
        self.message_store.append(self.ai.format_prompts(response, role="model"))

    def process_file(self, file) -> str:
        """Process a CSV file containing questions and answers.
        
        Args:
            file: A file object containing CSV data with Question and Answer columns.
            
        Returns:
            str: A message indicating the success or failure of file processing.
        """
        df = pd.read_csv(file)
        required_cols = {"Question", "Answer"}
        if not required_cols.issubset(df.columns):
            return "CSV must contain 'Question' and 'Answer' columns."
        
        questions = df["Question"].tolist()
        answers = df["Answer"].tolist()
        self.db.add_documents(documents=questions, metadatas=[{"answer": a} for a in answers])
        
        return f"File `{file.name}` processed successfully."
    
    def __create_context(self, query_results) -> str:
        """Create a context string from query results for the LLM.
        
        Args:
            query_results: Results from the vector database query.
            
        Returns:
            str: Formatted context string containing relevant Q&A pairs.
        """
        context = "QA-Knowledge:\n"
        for doc, meta, distance in zip(query_results['documents'][0], 
                                     query_results['metadatas'][0],
                                     query_results['distances'][0]):
            if distance < 0.5:  # Only include results with distance less than 0.5
                context += f"Q: {doc}\nA: {meta.get('answer', 'N/A')}\n\n"
        return context


