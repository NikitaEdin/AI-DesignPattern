"""
Handles code analysis and simplified (light-weight) pattern identification.
"""

from typing import Dict, Any
from shared.llm_interface import LLMInterface
from agent_prompts import AgentPrompts

class CodeAnalyser:
    """Analyses the given code"""

    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.prompts = AgentPrompts()

    
    # 'One-Shot' prompt to analyse the code
    def analyse(self, code_snippet:str) -> Dict[str, Any]:
        """
        Analyse code for strengths and weaknesses
        
        Returns:
            Dict with: current_pattern, confidence, purpose, issues, strengths
        """

        try:
            prompt = self.prompts.create_analysis_prompt(code_snippet)
            response = self.llm.generate_response(prompt)
            return self._parse_analysis(response)
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'current_pattern': 'Unknown',
                'confidence': 0.0,
                'purpose': 'Unknown',
                'issues': [], 'strengths': []
            }

    # Print analysis        
    def display_analysis(self, analysis: Dict[str, Any]) -> None:
        """Display analysis results"""
        print(f"\nCurrent Pattern: {analysis.get('current_pattern', 'None')}")
        print(f"Confidence: {analysis.get('confidence', 0.0):.2f}")
        print(f"Purpose: {analysis.get('purpose', 'Unknown')}")

        # issues
        issues = analysis.get('issues', [])
        if issues:
            print(f"\nIssues identified: {len(issues)}")
            for issue in issues[:3]:
                print(f" - {issue}")
        
        # strengths
        strengths = analysis.get('strengths', [])
        if strengths:
            print(f"\nStrengths: {len(strengths)}")
            for strength in strengths[:2]:
                print(f" - {strength}")

    def _parse_analysis(self, response: str) -> Dict[str, Any]:
        """Parse LLM response"""
        result = {
            'current_pattern': 'None',
            'confidence': 0.5,
            'purpose': 'Unknown',
            'issues': [], 'strengths': []
        }

        # Read each line
        lines = response.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            # Pattern
            if line.startswith('PATTERN:'):
                result['current_pattern'] = line.split(':', 1)[1].strip()
            # Confidence
            elif line.startswith('CONFIDENCE:'):
                try:
                    result['confidence'] = float(line.split(':', 1)[1].strip())
                except ValueError:
                    pass
            # Purpose
            elif line.startswith('PURPOSE:'):
                result['purpose'] = line.split(':', 1)[1].strip()
            # Issues
            elif line.startswith('ISSUES:'):
                current_section = 'issues'
            # Strengths
            elif line.startswith('STRENGTHS:'):
                current_section = 'strengths'
            elif line.startswith('-') and current_section:
                result[current_section].append(line[1:].strip())
        
        return result


        