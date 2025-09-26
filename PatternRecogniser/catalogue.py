from enum import Enum
import os
from typing import Final

# Workflow type
class WorkflowType(str, Enum):
    SINGLE_PROMPT = "single_prompt"
    MULTI_LAYERED = "multi_layered"

# Availabvle patterns
# Using Tuple for immutability (as it's final)
DESIGN_PATTERNS: Final[tuple[str, ...]] = (
    "Singleton", "Factory", "Builder", "Prototype",
    "Adapter", "Decorator", "Facade", "Proxy",
    "Observer", "Strategy", "Command", "Iterator", "State"
)

# Available difficulty levels
DIFFICULTY_LEVELS: Final[tuple[str, ...]] = ("E", "M", "H")

# LLM providers
LLM_PROVIDERS: Final[tuple[str, ...]] = (
    "openai", "claude", "kimi", "grok", "ollama"
)

LLM_SHORT_MAP: Final[dict[str, str]] = {
    "o": "openai",
    "c": "claude",
    "kimik2": "kimi",
    "grok4f": "grok",
    "l": "ollama",
}


############### UTILS ###############

def get_llm_prefix(name:str) -> str:
    for prefix, provider in LLM_SHORT_MAP.items():
        if provider == name:
            return prefix
    
    return None

def is_file_generated_by_llm(filename: str, llm_name: str) -> bool:
    # get prefix from given llm name
    expected_prefix = get_llm_prefix(llm_name)
    if expected_prefix is None:
        return False
    
    # Extract just the filename
    filename = os.path.basename(filename)
    
    # Abort is file is not a python script
    if not filename.endswith(".py"):
        return False
    
    # Split formatted filename structure
    parts = filename[:-3].split("_")
    if len(parts) < 4:
        return False
    
    # Get file llm_prefix and compare
    file_prefix = parts[-1]
    return file_prefix == expected_prefix