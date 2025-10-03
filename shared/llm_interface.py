"""
LLM interface Module

Provides unified interface for different LLM providers.
"""

import os
from typing import Dict, List, Type
import requests
from abc import ABC, abstractmethod
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

#### Direct AI Providers ####

class OllamaInterface(LLMInterface):
    """Ollama LLM interface"""

    def __init__(self, model: str = "codellama", host: str = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b-instruct")
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
                max_completion_tokens=5000
            )
        
            if not response.choices:
                raise Exception("No choices returned from OpenAI API")

            result = response.choices[0].message.content
        
            # Handle empty/None results
            if not result:
                raise Exception("Empty response content from OpenAI API")
                
            if len(result.strip()) == 0:
                raise Exception("Response content is only whitespace")
            
            return result.strip()
            
        except Exception as e:
            print(f"Exception caught: {e}")
            raise Exception(f"OpenAI API error: {str(e)}")
        
    def get_prefix(self) -> str:
        return "O"

class ClaudeInterface(LLMInterface):
    """Interface for Claude LLM"""

    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("Claude API Key is required")
        
    def generate_response(self, prompt: str) -> str:
        """Generate response using Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
        

    def get_prefix(self) -> str:
        return "C"


#### OpenRouter AI PROVIDER ####
class OpenRouterInterface(LLMInterface):
    """Base interface for OpenRouter LLMs"""
    def __init__(self, api_key:str = None, model: str = None, max_tokens: int = 5000, temperature: float = 0.7):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.base_url = "https://openrouter.ai/api/v1"

        if not self.api_key:
            raise ValueError("OpenRouter API Key is required")
        if not self.model:
            raise ValueError("Model is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": os.getenv("APP_URL", "http://localhost"),
            "X-Title": os.getenv("APP_NAME", "OpenRouter Interface"),
            "Content-Type": "application/json"
        }

    def generate_response(self, prompt):
        """Generate response using OpenRouter """
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")


    def get_prefix(self):
        return "OR"

#### Specific OpenRouter model classes ####
class GrokInterface(OpenRouterInterface):
    """Interface for Grok via OpenRouter"""
    # 1.12T
    def __init__(self, api_key = None, model = None, max_tokens = 5000, temperature = 0.7):
        super().__init__(api_key, "x-ai/grok-code-fast-1", max_tokens, temperature)

    def get_prefix(self):
        return "GROK"
    
class QwenInterface(OpenRouterInterface):
    # Limited rate limit of 50 per date (qwen/qwen3-coder:free)

    """Interface for Qwen3 Coder via OpenRouter"""
    # 48B
    def __init__(self, api_key = None, model = None, max_tokens = 5000, temperature = 0.7):
        super().__init__(api_key, "qwen/qwen3-coder", max_tokens, temperature)

    def get_prefix(self):
        return "Q3C"
    
# Free models
class Grok4FastInterface(OpenRouterInterface):
    # Fast and high quality results, no limits, even after 1.5M tokens in a day.
    """Interface for Grok 4 Fast (free) via OpenRouter"""
    def __init__(self, api_key = None, model = None, max_tokens = 5000, temperature = 0.7):
        super().__init__(api_key, "x-ai/grok-4-fast:free", max_tokens, temperature)

    def get_prefix(self):
        return "GROK4F"
    
class KimiK2Interface(OpenRouterInterface):
    # HIGH failure rate with kimi-k2:free (uses prompts&answers for public datasets)
    # low but recoverable failure rate with kimi-k2 (paid)
    # free tier is limited to low requested tokens
    
    """Interface for MoonshotAI: Kimi K2 0711 via OpenRouter"""
    def __init__(self, api_key = None, model = None, max_tokens = 5000, temperature = 0.7):
        super().__init__(api_key, "moonshotai/kimi-k2-0905", max_tokens, temperature)

    def get_prefix(self):
        return "KimiK2"

#### Factory ####

class LLMFactory:
    """Factory class to create LLM interfaces"""


    # Registery of available providers
    _providers: Dict[str, Type[LLMInterface]] = {
        # Direct providers
        "ollama": OllamaInterface,
        "openai": OpenAIInterface,
        "claude": ClaudeInterface,

        # OpenRouter
        "grok": GrokInterface, 
        "qwen": QwenInterface, # limited to 50 requests per days
        "grok4fast": Grok4FastInterface, #free
        "kimi": KimiK2Interface # limited max tokens
    }

    @staticmethod
    def create_llm(provider: str, **kwargs) -> LLMInterface:
        provider = provider.lower()
        if provider not in LLMFactory._providers:
                raise ValueError(f"Unsupported LLM provider: {provider}")
            
        return LLMFactory._providers[provider](**kwargs)
        
    @staticmethod
    def get_available_providers() -> List[str]:
        return tuple(LLMFactory._providers.keys())