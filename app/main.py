from typing import Any
import pandas as pd
from .llm import GoogleGeminiLLM
from .prompt import QA_SYSTEM_PROMPT
from .db import ChromaDBManager


class Chat:
    def __init__(self):
        self.message_store = []
        self.ai = GoogleGeminiLLM(system_prompt=QA_SYSTEM_PROMPT)
        self.db = ChromaDBManager()

    
    def __call__(self, user_message) -> Any:
        context = self.__create_context(self.db.query_documents(user_message))
        user_message = f"{context}\n\n{user_message}"
        self.message_store.append(self.ai.format_prompts(user_message, role="user"))
        response = ""
        for chunk in self.ai.generate_text(self.message_store):
            if isinstance(chunk, str):
                response += chunk
                yield chunk
        self.message_store.append(self.ai.format_prompts(response, role="model"))

    def process_file(self,file) -> str:
        df = pd.read_csv(file)
        required_cols = {"Question", "Answer"}
        if not required_cols.issubset(df.columns):
            return "CSV must contain 'Question' and 'Answer' columns."
        
        questions = df["Question"].tolist()
        answers = df["Answer"].tolist()
        self.db.add_documents(documents=questions, metadatas=[{"answer": a} for a in answers])
        
        return f"File `{file.name}` processed successfully."
    
    def __create_context(self, query_results) -> str:
        context = "QA Context:\n"
        for doc, meta, distance in zip(query_results['documents'][0], 
                                     query_results['metadatas'][0],
                                     query_results['distances'][0]):
            if distance < 0.5:  # Only include results with distance less than 0.5
                context += f"Q: {doc}\nA: {meta.get('answer', 'N/A')}\n\n"
        return context


