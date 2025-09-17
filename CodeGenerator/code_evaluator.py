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
TASK: Evaluate the following Python code snippet to determine if it correctly implements the {design_pattern} design pattern, *without ever disclosing the pattern name**.

Design Pattern: {design_pattern}
Exepected Difficulty: {difficulty_desc}

Code to evaluate:
```python
{code}
```

EVALUATION CRITERIA (ALL must pass for PASS rating):
1. Pattern Implementation: Does the code correctly implement the {design_pattern} design pattern structure?
2. Key Components: Are all essential components and relationships of the pattern present?
3. Syntax & Execution: Is the code syntactically correct and runnable?
4. Difficulty Match: Does the complexity and length match the expected difficulty level?
5. Code Quality: Are there any bugs, logic errors, or major issues?
6. NAMING VIOLATION CHECK: Any class, method, or variable names containing "{design_pattern}" or variations MUST result in FAIL.

RESPONSE FORMAT:
EVALUATION: [PASS/FAIL]
FEEDBACK: [Detailed explanation covering: what's implemented correctly, what's missing/wrong, difficulty appropriateness, and any naming violations]

Example Response:
EVALUATION: PASS
FEEDBACK: The code correctly implements the Singleton pattern by ensuring only one instance of the class is created.
"""
        
        return prompt
    
    def _parse_evaluation_response(self, response: str) -> Tuple[bool, str]:
        """ Parse LLM evaluation response """
        try:
            lines = response.strip().split('\n')
            evaluation, feedback = None, None
            
            for i, line in enumerate(lines):
                if line.upper().startswith('EVALUATION:'):
                    evaluation = line.split(':', 1)[1].strip().upper()
                elif line.upper().startswith('FEEDBACK:'):
                    feedback = '\n'.join(lines[i:]).split(':', 1)[1].strip()
                    break
                    
            if not evaluation or not feedback:
                print(f"[DEBUG] RESPONSE PRINT\n{response}")
                return False, f"Missing EVALUATION or FEEDBACK in response"
                
            return evaluation == "PASS", feedback
            
        except Exception as e:
            return False, f"Parse error: {str(e)}"
        
    def get_retry_prompt(self, original_prompt: str, feedback: str) -> str:
        """ Generate a retry prompt based on feedback """
        retry_prompt = f"""
RETRY ATTEMPT - PREVIOUS VERSION FAILED

CRITICAL: You MUST follow the exact output format requirements from the original prompt.

PREVIOUS ATTEMPT FEEDBACK:
{feedback}

MANDATORY IMPROVEMENTS REQUIRED:
1. Address ALL issues mentioned in the feedback above
2. Ensure EXACT format compliance: ```python ... ```
3. Return ONLY code within code blocks - NO explanations or text outside
4. Verify syntax correctness before responding
5. Double-check pattern implementation requirements

FORMAT REMINDER (CRITICAL):
- Start response immediately with ```python
- End with ```
- NO text before or after code blocks
- NO explanations or comments outside the code

{original_prompt}

FINAL REMINDER: This is a retry attempt. Learn from the feedback and ensure you address every issue mentioned while maintaining perfect format compliance.
"""
        return retry_prompt