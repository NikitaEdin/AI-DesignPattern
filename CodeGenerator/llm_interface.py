"""
LLM interface Module

Provides unified interface for different LLM providers.
"""



import os
import requests
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMInterface(ABC):
    """Abstract base class for LLM interfaces"""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate response from LLM"""
        pass

    @abstractmethod
    def get_prefix(self) -> str:
        """Get prefix identifier for LLM"""
        pass


class OllamaInterface(LLMInterface):
    """Ollama LLM interface"""

    def __init__(self, model: str = "codellama", host: str = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "codellama:latest")
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        

    def generate_response(self, prompt: str) -> str:
        """ Generate response from Ollama LLM """
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }

            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            return result.get('response', '').strip()
        except requests.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")

    def get_prefix(self) -> str:
        return "L"
    


class OpenAIInterface(LLMInterface):
    """Interface for OpenAI LLM"""

    def __init__(self, api_key: str = None, model: str = "gpt-5-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
    def generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI API"""

        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=3000
            )
            
            result = response.choices[0].message.content
            return result
            
        except Exception as e:
            print(f"Exception caught: {e}")
            raise Exception(f"OpenAI API error: {str(e)}")
        
    def get_prefix(self) -> str:
        return "O"


# TODO: Implement Claude, and Kimi K2 interfaces



class LLMFactory:
    """Factory class to create LLM interfaces"""

    @staticmethod
    def create_llm(provider: str, **kwargs) -> LLMInterface:
        provider = provider.lower()
        if provider == "ollama":
            return OllamaInterface(**kwargs)
        elif provider == "openai":
             return OpenAIInterface(**kwargs)
        # elif provider == "claude":
        #     return ClaudeInterface(**kwargs)
        # elif provider == "kimi":
        #     return KimiK2Interface(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
    @staticmethod
    def get_availabvle_providers() -> list:
        return ["ollama", "openai"]  