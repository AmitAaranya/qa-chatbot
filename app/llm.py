import os
from typing import Literal
from google import genai
from google.genai import types


class GoogleGeminiLLM:
    def __init__(self, system_prompt:str = "You are a helpful assistant."):
        api_key = os.environ["GOOGLE_GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        self.generate_content_config = types.GenerateContentConfig(
                                temperature=0.3,
                                system_instruction=[types.Part.from_text(text=system_prompt)]
                                )


    def format_prompts(self, content:str, role:Literal["user", "model"]):
        return types.Content(role=role, parts=[types.Part(text=content)])


    def generate_text(self, prompts:list, tools=None):
        self.response = self.client.models.generate_content_stream(
                    model="gemini-2.5-flash-lite", 
                    contents=prompts,
                    config=self.generate_content_config,
                    
                )
        for chunk in self.response:
            if chunk.text:
                yield chunk.text
            else:
                yield self.__process_chunk(chunk)


    def __process_chunk(self, chunk):
        ...