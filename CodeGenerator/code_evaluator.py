"""
Code Evaluator Module

Handles the evlauation of generated code snippets
"""

from typing import Tuple
from llm_interface import LLMInterface
import re

class CodeEvaluator:
    """Evaluates generated code for corrrectness and pattern compliance"""

    def __init__(self, llm: LLMInterface):
        self.llm = llm

    def evaluate_code(self, code: str, design_pattern: str, difficulty: str) -> Tuple[bool, str]:
        """
        Evaluate if generated code correctly implements the given design pattern.

        Args:
            code (str): The generated code snippet.
            design_pattern (str): The design pattern to check against.
            difficulty (str): The difficulty level of the design pattern.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating correctness and feedback message.
        """

        evaluation_prompt = self._create_evaluation_prompt(code, design_pattern, difficulty)

        try:
            evaluation_response = self.llm.generate_response(evaluation_prompt)
            is_valid, feedback = self._parse_evaluation_response(evaluation_response)
            return is_valid, feedback
        except Exception as e:
            return False, f"Evaluation failed: {str(e)}"
        
    def _create_evaluation_prompt(self, code: str, design_pattern: str, difficulty: str) -> str:
        """ Create evaluation prompt for LLM"""
        difficulty_map = {
            'E': 'Easy - Basic implementation with core pattern elements',
            'M': 'Medium - Standard implementation with additional features',
            'H': 'Hard - Complex implementation with advanced features, optimizations, and edge cases'
        }

        difficulty_desc = difficulty_map.get(difficulty, 'Unknown difficulty')

        prompt = f"""
You are a code reviewer specialising in design patterns. 
Evaluate the following Python code snippet to determine if it correctly implements the {design_pattern} design pattern.

Design Pattern: {design_pattern}
Exepected Difficulty: {difficulty_desc}

Code to evaluate:
```python
{code}
```

Evaluate based on these criteria:
1. Does the code correctly implement the {design_pattern} design pattern?
2. Are the key components and relationships of the pattern present?
3. Is the code syntactically correct and runnable?
4. Does the complexity match the expected difficulty level?
5. Are there any obvious bugs or issues?

Response in the following format:
EVALUATION: [PASS/FAIL]
FEEDBACK: [Detailed explanation of your evaluation, including what's correct, what's missing, or what needs improvement]

Example Response:
EVALUATION: PASS
FEEDBACK: The code correctly implements the Singleton pattern by ensuring only one instance of the class is created.
"""
        
        return prompt
    
    def _parse_evaluation_response(self, response: str) -> Tuple[bool, str]:
        """ Parse LLM evaluation response """

        try:
            eval_match = re.search(r"EVALUATION:\s*(PASS|FAIL)", response, re.IGNORECASE)
            feedback_match = re.search(r"FEEDBACK:\s*(.*)", response, re.IGNORECASE | re.DOTALL)

            if not eval_match or not feedback_match:
                return False, "Invalid evaluation response format."

            evaluation = eval_match.group(1).strip().upper()
            feedback = feedback_match.group(1).strip()

            is_valid = evaluation == "PASS"
            return is_valid, feedback
        except Exception as e:
            # If parsing fails - assume failure and provide error feedback
            return False, f"Could not parse evaluation response: {str(e)}"
        
    def get_retry_prompt(self, original_prompt: str, feedback: str) -> str:
        """ Generate a retry prompt based on feedback """
        retry_prompt = f"""
{original_prompt}

PREVIOUS ATTEMPT FEEDBACK:
{feedback}

Please generate an improved version that addresses the feedback above.
Make sure to correctly implement the design pattern and fix any identified issues.
"""
        return retry_prompt