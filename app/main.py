from typing import Any
from .llm import GoogleGeminiLLM


class Chat:
    def __init__(self):
        self.message_store = []
        self.ai = GoogleGeminiLLM()

    
    def __call__(self, user_message) -> Any:
        self.message_store.append(self.ai.format_prompts(user_message, role="user"))
        response = ""
        for chunk in self.ai.generate_text(self.message_store):
            if isinstance(chunk, str):
                response += chunk
                yield chunk
        self.message_store.append(self.ai.format_prompts(response, role="model"))


