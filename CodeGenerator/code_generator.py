""" 
Code Generator Module

Handles the generation of code snippets
"""

import time
import re
from typing import Tuple
from llm_interface import LLMInterface
from code_evaluator import CodeEvaluator

class CodeSnippetGenerator: 
    """ Generate code snippets using specified design patterns """

    def __init__(self, llm: LLMInterface, max_retries: int = 5):
        self.llm = llm
        self.evaluator = CodeEvaluator(llm)
        self.max_retries = max_retries

        # Design pattern template for different difficulty levels
        # self.difficulty_templates = {
        #     'E': "Create the simplest possible implementation that demonstrates only the core concept. Keep it minimal with no extra features or optimizations. Limit to 15-25 lines of code maximum.",
        #     'M': "Create a practical implementation that demonstrates the core concept with realistic usage. Include basic error handling and meaningful naming, but keep the implementation concise - aim for 30-50 lines of code total. Focus on one key additional feature beyond the core concept.",
        #     'H': "Create a robust implementation with advanced features and edge case handling. Despite the complexity, keep the code concise and well-structured - target 60-100 lines maximum. Prioritize depth over breadth: choose 2-3 key advanced features rather than trying to cover everything."
        # }

        self.difficulty_templates = {
            'E': "Create the simplest possible implementation that demonstrates only the core concept. Keep it minimal with no extra features or optimizations. Limit to under 50 lines of code in total.",
            'M': "Create a practical implementation that demonstrates the core concept with realistic usage. Include basic error handling and meaningful naming, but keep the implementation concise. Aim for 30 - 100 lines of code in total.",
            'H': "Create a robust implementation with advanced features and edge case handling. Despite the complexity, keep the code concise and well-structured. aim for 80 - 200 lines of code in total."
        }


    def generate_code_snippet(self, design_pattern: str, difficulty: str) -> Tuple[str, bool, str]:
        """ Generate code snippet for the given design pattern and difficulty level 
        
        Args:
            design_pattern (str): The design pattern to implement.
            difficulty (str): The difficulty level ('E', 'M', 'H').

        Returns:
            Tuple of (generated_code: str, is_valid: bool, feedback: str)
        """

        # Initial generation prompt
        prompt = self._create_generation_prompt(design_pattern, difficulty)

        for attempt in range(self.max_retries):
            try:
                # generate code
                generated_code = self.llm.generate_response(prompt)
                # Clean and extract
                clean_code = self._extract_python_code(generated_code)

                if not clean_code:
                    if attempt < self.max_retries - 1:
                        prompt = self._create_retry_prompt(prompt, "No valid Python code found.")
                        time.sleep(2)
                        continue
                    else:
                        return "", False, "Failed to generate a valid Python code snippet."
                    
                # Evluate the generated code
                is_valid, feedback = self.evaluator.evaluate_code(clean_code, design_pattern, difficulty)

                # DEBUG
                #print(feedback)

                if is_valid:
                    return clean_code, True, feedback
                else:
                    if attempt < self.max_retries - 1:
                        print(f"Attempt {attempt + 1} failed, retrying...")
                        prompt = self.evaluator.get_retry_prompt(prompt, feedback)
                        time.sleep(2)
                        continue
                    else:
                        return clean_code, False, feedback
                    

            except Exception as e:
                if attempt < self.max_retries - 1:
                    prompt = self._create_retry_prompt(prompt, f"Generation error: {str(e)}")
                    time.sleep(2)
                    continue
                else:
                    return "", False, f"Generation failed after {self.max_retries} attempts: {str(e)}"
                
        return "", False, "Maximum retries exceeded."
    
    def _create_generation_prompt(self, design_pattern: str, difficulty: str) -> str:
        """ Create the actual code generation prompt """
        difficulty_desc = self.difficulty_templates.get(difficulty, "")

        prompt = f"""
TASK: Generate a Python code snippet that implements the {design_pattern} design pattern.

CRITICAL OUTPUT FORMAT REQUIREMENTS:
- Return ONLY Python code within ```python ... ``` code blocks
- NO explanations, comments, or additional text outside the code block
- Start your response immediately with ```python
- End with ```

Requirements:
- Difficulty Level: {difficulty} - ({difficulty_desc})
- Include proper class definitions, methods, attributes, and relationships.
- Make the code executable and demonstate usage within a main section.
- Ensure the code is syntactically correct and follows Python best practices.
- NEVER use the word "{design_pattern}" or any variation of it in class names, method names, variable names, or comments.


Provide a complete, working Python implementation that clearly demonstrates the {design_pattern} design pattern.

Make sure to:
1. Implement all key components of the {design_pattern} pattern.
2. Use meaningful class and method names, but avoid using the pattern name directly.
3. Add a usage example in a main section.
5. Ensure the code is free of syntax errors.

Return only the Python code, formatted properly, no explanation, comments, or additional text.
Provide the code within ````python ... ``` blocks.

FORMAT EXAMPLE:
```python
# Your code here
```

        """
        return prompt

    def _extract_python_code(self, response: str) -> str:
        """ Extract Python code from LLM response """
        # Look code blocks first
        code_block_pattern = r'```(?:python)?\s*\n(.*?)\n```'
        matches = re.findall(code_block_pattern, response, re.DOTALL)

        if matches:
            return matches[0].strip()
        
        # If no code blocks found, try extract Python-like content
        # TODO: More sophisticated extraction if needed

        # If no code block, assume entire response is code
        return response.strip()


    def _create_retry_prompt(self, original_prompt: str, error_message: str) -> str:
        """ Create a retry prompt based on error message """
        retry_prompt = f"""
{original_prompt}

ISSUE WITH PREVIOUS ATTEMPT:
{error_message}

Generate a corrected version that addresses the issue above.
"""
        return retry_prompt

############ TESTING ############

    def add_noise(self, code_snippet:str) -> str:
        prompt = self._create_noise_prompt(code_snippet)
        noised_code = self.llm.generate_response(prompt)
        return noised_code


    def _create_noise_prompt(self, code_snippet: str) -> str:
        prompt = f"""
You are given a Python code snippet that demonstrates a design pattern.

YOUR TASK:
- Keep the code intact and functional.
- Do NOT alter the overall structure of the pattern.
- Stay within one file.
- Do not include any comments in the final code.
- Do not use triple backticks or any code block markers in the output.
- Only return the final transformed code.

Add realistic 'noise' by applying **at least two different noise types** from this list:
1. **Domain-specific naming**: Replace generic names with domain/business terms.
2. **Extra/useless functions and classes**: Add functions or lightweight classes that serve no real purpose, but look plausible.
3. **Additional responsibilities**: Add logging, validation, or error handling around key operations.
4. **Non-essential functionality**: Add extra methods or classes that is unrelated but plausible (e.g., data formatting, config loading).
5. **Inline complexity**: Introduce minor conditionals or branching logic inside methods (e.g., input checks, default handling).

CODE SNIPPET:
```python
{code_snippet}
```
"""
        return prompt
        