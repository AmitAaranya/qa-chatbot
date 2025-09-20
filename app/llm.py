import os
from typing import Literal
from google import genai
from google.genai import types


class GoogleGeminiLLM:
    """A class to interact with Google's Gemini LLM for text generation.
    
    This class provides methods to format prompts and generate text responses
    using Google's Gemini language model.
    """
    
    def __init__(self, system_prompt:str = "You are a helpful assistant."):
        """Initialize the Gemini LLM client.
        
        Args:
            system_prompt (str, optional): The system prompt to set the behavior of the model.
                Defaults to "You are a helpful assistant.".
        """
        api_key = os.environ["GOOGLE_GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        self.generate_content_config = types.GenerateContentConfig(
                                temperature=0.3,
                                system_instruction=[types.Part.from_text(text=system_prompt)]
                                )


    def format_prompts(self, content:str, role:Literal["user", "model"]):
        """Format content into a prompt structure expected by the Gemini model.
        
        Args:
            content (str): The text content of the prompt.
            role (Literal["user", "model"]): The role associated with the content.
        
        Returns:
            types.Content: A formatted prompt object.
        """
        return types.Content(role=role, parts=[types.Part(text=content)])


    def generate_text(self, prompts:list, tools=None):
        """Generate text responses from the Gemini model in a streaming fashion.
        
        Args:
            prompts (list): A list of formatted prompts to send to the model.
            tools (Optional): Function tools to provide to the model. Defaults to None.
        
        Yields:
            str: Generated text chunks from the model.
        """
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