from enum import Enum
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
    "grok": "grok",
    "l": "ollama",
}