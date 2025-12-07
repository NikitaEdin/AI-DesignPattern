"""
Agent Prompts

A collection of all available prompts for the recommender to use
"""

from typing import Dict, Any, List
from catalogue import DESIGN_PATTERNS

class AgentPrompts:
    """Holds all prompt templates"""



    def create_analysis_prompt(self, code_snippet: str) -> str:
        """Create prompt for code analysis"""
        return f"""
You're an expert in Design Pattern Recommender analysing Python code.

AVAILABLE DESIGN PATTERNS:
{", ".join(DESIGN_PATTERNS)}

CODE TO ANALYSE:
```python
{code_snippet}
```

Provide a structrued analysis using this EXACT format:

PATTERN: [Pattern name or "None"]
CONFIDENCE: [0.0-1.0]
PURPOSE: [Short high-level purpose of this code]

ISSUES:
- [Issue 1]
- [Issue 2]
- [Or "None identified"]

STRENGTHS:
- [Strength 1]
- [Strength 2]

Focus on:
1. Identifying any existing design patterns
2. Understanding the code's purpose
3. Finding potential issues or limitations
4. Recognising good practices
"""