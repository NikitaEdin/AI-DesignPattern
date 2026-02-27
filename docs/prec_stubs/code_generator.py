"""
Code Generator

Generates improved code based on recommendations
"""

from typing import Dict, Any
from shared.llm_interface import LLMInterface
from PatternRecommender.agent_prompts import AgentPrompts

class CodeGenerator:
    """Generate improved code based on recommendations"""

    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.prompts = AgentPrompts()

    def generate_improved_code(
            self, original_code: str, recommendation: Dict[str, Any], filename: str) -> str:
        """Improves given code based on recommendation"""

        try:
            prompt = self.prompts.create_code_generation_prompt(original_code, recommendation, filename)
            response = self.llm.generate_response(prompt)
            return self._extract_code(response)
        except Exception as e:
            return f'[Error] Failed to generate code: {str(e)}'
        

    def request_user_approval(self) -> bool:
        """Request user approval for code generation"""
        
        while True:
            response = input("\nGenerate improved code? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                print("\nGenerating improved code...")
                return True
                
            elif response in ['no', 'n']:
                print("\nSkipping code generation. Keeping original code.")
                return False
            else:
                print("Please answer 'yes' or 'no'")
    
    def _extract_code(self, response: str) -> str:
        """Extract code from code-chunk"""
        if '```python' in response:
            parts= response.split('```python')
            if len(parts) > 1:
                return parts[1].split('```')[0].strip()
            
        if '```' in response:
            parts = response.split('```')
            if len(parts) > 2:
                return parts[1].strip()
            
        return response.strip()
            
