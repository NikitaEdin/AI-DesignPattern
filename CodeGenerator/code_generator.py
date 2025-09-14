""" 
Code Generator Module

Handles the generation of code snippets
"""

import re
from typing import Tuple
from llm_interface import LLMInterface
from code_evaluator import CodeEvaluator

class CodeSnippetGenerator: 
    """ Generate code snippets using specified design patterns """

    def __init__(self, llm: LLMInterface, max_retries: int = 3):
        self.llm = llm
        self.evaluator = CodeEvaluator(llm)
        self.max_retries = max_retries

        # Design pattern template for different difficulty levels
        self.difficulty_templates = {
            'E': "Create a simple, basic implementation that clearly demonstratres the core concept.",
            'M': "Create a standard implementation with proper error handling and additional features.",
            'H': "Create a complex implementation with advanced features, optimisations, and edge cases."
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
                        prompt = self._create_retry_prompt(design_pattern, difficulty, "No valid Python code found.")
                        continue
                    else:
                        return "", False, "Failed to generate a valid Python code snippet."
                    
                # Evluate the generated code
                is_valid, feedback = self.evaluator.evaluate_code(clean_code, design_pattern, difficulty)

                if is_valid:
                    return clean_code, True, feedback
                else:
                    if attempt < self.max_retries - 1:
                        prompt = self.evaluator.get_retry_prompt(prompt, feedback)
                    else:
                        return clean_code, False, feedback
                    

            except Exception as e:
                if attempt < self.max_retries - 1:
                    prompt = self._create_retry_prompt(prompt, f"Generation error: {str(e)}")
                    continue
                else:
                    return "", False, f"Generation failed after {self.max_retries} attempts: {str(e)}"
                
        return "", False, "Maximum retries exceeded."
    
    def _create_generation_prompt(self, design_pattern: str, difficulty: str) -> str:
        """ Create the actual code generation prompt """
        difficulty_desc = self.difficulty_templates.get(difficulty, "")

        prompt = f"""
Generate a Python code snippet that implements the {design_pattern} design pattern.

Requirements:
- Difficulty Level: {difficulty} - ({difficulty_desc})
- Include proper class definitions, methods, attributes, and relationships.
- Make the code executable and demonstate usage within a main section.
- Ensure the code is syntactically correct and follows Python best practices.
- Follow Python best practices and PEP 8 style guidelines.

CRITICAL NAMING CONSTRAINTS:
- NEVER use the word "{design_pattern}" or any variation of it in class names, method names, variable names, or comments

Design Pattern: {design_pattern}

Provide a complete, working Python implementation that clearly demonstrates the {design_pattern} design pattern.

Make sure to:
1. Implement all key components of the {design_pattern} pattern.
2. Use meaningful class and method names, but avoid using the pattern name directly.
3. Add a usage example in a main section.
4. Ensure the code is completely free of the pattern name in ANY form
5. Ensure the code is free of syntax errors.

Return only the Python code, formatted properly, no explanation, comments, or additional text.
Provide the code within ````python ... ``` blocks.
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


        