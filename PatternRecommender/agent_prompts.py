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
    

    def create_question_prompt(self, code_snippet: str,
                               analysis: Dict[str, Any],
                               insights: List[Dict[str, str]]) -> str:
        """Create promot for generating clarifying questions about code context"""

        # Build conversation history
        history = ''
        if insights:
            history = '\n\nPrevious Q&A:\n'
            for i, insight in enumerate(insights, 1):
                history += f'{i}. Q: {insight['question']}\nA:{insight['answer']}\n'

        # Extract insight points
        current_pattern = analysis.get('current_pattern', 'Not identified')
        purpose = analysis.get('purpose', 'Not yet determined')
        issues = analysis.get('issues', [])

        return f"""
You are an expert in code consultant, helping understand code context to provide better recommendations.

CODE CONTEXT:
- Identified Pattern: {current_pattern}
- Apparent Purpose: {purpose}
- Potential Issues Found: {len(issues)}
{history}

YOUR TASK:
Generate ONE focused question to clarify the code's context, usage, or goals. 
This information will help recommend appropriate design patterns or implementation improvements.

WHAT TO EXPLORE:
1. **Business Context**: What problem does this solve? What's the real-world use case?
2. **Integration Points**: What other systems/components interact with this code?
3. **Pain Points**: What's not working well? What needs improvement?
4. **Constraints**: Any technical, business, or team limitations to consider?
5. **Future Direction**: Expected changes, growth, or new requirements?

QUESTION GUIUDELINES:
- Use plain, conversation language.
- Keep questions under 25 words.
- Ask about ONE specific aspect at a time.
- Focus on context and goals, not implementation details.
- Be specific enough to get actionable answers.
- Avoid assumptions about technical expertise.

GOOD QUESTIONS:
- "What's the biggest problem you're experiencing with this code right now?"
- "How often do you expect to add new types or variants of this functionality?"
- "What parts of this logic change frequently, and what parts stay the same?"
- "Do you need different ways to do this same operation depending on the situation?"

WHEN TO STOP:
If you have sufficient information about:
- The code's purpose.
- How and when it's used.
- Current problems or limitations.
- What improvements are needed.

Then respond with: NO_MORE_QUESTIONS

OTHERWISE FORMAT YOUR RESPONSE AS:
QUESTION: [your clear, focused question here]
REASON: [brief explanation of what insight this will provide - optional, only if it helps]

Code snippet for reference:
```python
{code_snippet}

"""