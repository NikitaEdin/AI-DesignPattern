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
    
    def create_recommendation_prompt(
        self,
        code_snippet: str,
        analysis: Dict[str, Any],
        insights: List[Dict[str, str]]
    ) -> str:
        """Create prompt for recommendation"""
        
        context = ""
        if insights:
            context = "\n\nInsights from conversation:\n"
            for insight in insights:
                context += f"Q: {insight['question']}\nA: {insight['answer']}\n"
        
        return f"""
You are an expert in code recommendation for improving code using design patterns.

Available Design Patterns:
{", ".join(DESIGN_PATTERNS)}

ANALYSIS:
- Current Pattern: {analysis.get('current_pattern', 'None')}
- Confidence: {analysis.get('confidence', 0.0)}
- Purpose: {analysis.get('purpose', 'Unknown')}
- Issues: {', '.join(analysis.get('issues', ['None']))}
- Strengths: {', '.join(analysis.get('strengths', ['None']))}

CONTEXT:
{context}

CONSIDER ALL OPTIONS:
1. Keep current pattern (if appropriate).
2. Improve current implementation (if pattern is right but flawed).
3. Switch to different pattern (if better suited).
4. Add design pattern (if would benefit).
5. Remove design pattern (if adds complexity or over-engineered for its scale/purpose).
6. No changes needed (if fine as-is).


Provide recommendation in this EXACT format:

RECOMMENDATION: [KEEP_CURRENT / IMPROVE_CURRENT / CHANGE_PATTERN / ADD_PATTERN / REMOVE_PATTERN / NO_CHANGE]
PATTERN: [Pattern name or "None"]
CONFIDENCE: [0.0-1.0]

RATIONALE:
[Briefly explain why this recommendation makes sense]

BENEFITS:
[Expected improvements - short]

CONSIDERATIONS:
Be pragmatic: Not every code needs a design pattern. Favour simplicity unless complexity is justified.

META-EVALUATION GUIDELINES:
1. Complexity Check: If the code's primary purpose is singular, fixed, and under 20 lines, the default recommendation is NO_CHANGE.
2. Principle Check: Only recommend a pattern (like Strategy or Observer) if the resulting code is demonstrably easier to extend (OCP) *and* the code is expected to change frequently or handle multiple, distinct algorithms in the future.
3. Over-Engineering Penalty: If the suggested pattern adds more than 50% boilerplate code (interfaces, abstract classes, context managers) to solve the simple problem, reject the pattern.
"""

    def create_code_generation_prompt(
            self, original_code: str, recommendation: Dict[str, Any], filename:str
    ) -> str:
        """Prompt for generating new or improved code"""
        return f"""
You're an expert writing clean and professional code by utilising design patterns improvements.

ORIGINAL FILE: {filename}

RECOMMENDATION:
- Type: {recommendation.get('recommendation_type', 'Unknown')}
- Pattern: {recommendation.get('suggested_pattern', 'None')}
- Rationale: {recommendation.get('rationale', 'N/A')}

ORIGINAL CODE:
```python
{original_code}
```

TASK: Generate the improved version following the recommendation.

REQUIREMENTS:
1. Implement the suggested pattern correctly.
2. Preserve all functionality.
3. Maintain readability and best practices.
4. Add clear comments explaining pattern usage.
5. Include docstrings for classes and methods.

Provide ONLY the complete Python code in triple backticks:

```python
# Your improved code here
```

"""
