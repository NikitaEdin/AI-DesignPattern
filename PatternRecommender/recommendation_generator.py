"""
Recommendation Generator

Generates design pattern recommendations based on analysis and conversation.
"""

from typing import Dict, Any, List
from shared.llm_interface import LLMInterface
from agent_prompts import AgentPrompts

class RecommendationGenerator:
    """Generates recommendations"""

    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.prompts = AgentPrompts()

    def generate_recommendation(
            self,  code_snippet: str,
            analysis: Dict[str, Any], insights: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate a design pattern recommendation

        Returns:
            Dict with recommendation_type, suggested_pattern, confidence, rationale, benefits, should_modify
        """

        try:
            prompt = self.prompts.create_recommendation_prompt(code_snippet, analysis, insights)
            response = self.llm.generate_response(prompt)
            return self._parse_recommendation(response, analysis)
        except Exception as e:
            return {
                'error': f"Recommendation failed: {str(e)}",
                'recommendation_type': 'NO_CHANGE',
                'current_pattern': analysis.get('current_pattern', 'None'),
                'suggested_pattern': 'None',
                'confidence': 0.0,
                'rationale': '', 'benefits': '',
                'should_modify': False
            }
        
    def display_recommendation_summary(self, recommendation: Dict[str, Any]) -> None:
        """Display recommendation summary"""
        rec_type = recommendation.get('recommendation_type', 'UNKNOWN')
        current_pattern = recommendation.get('current_pattern', 'None')
        suggested_pattern = recommendation.get('suggested_pattern', 'None')
        
        # Format user-friendly message based on recommendation type
        if 'REMOVE' in rec_type:
            print(f"\nRecommendation: Remove the {current_pattern} pattern\n\nReason: {recommendation.get('rationale', 'N/A')[:200]}...\n\nThe code would be simpler without this pattern.")
        elif 'CHANGE' in rec_type:
            print(f"\nRecommendation: Switch from {current_pattern} to {suggested_pattern}\n\nReason: {recommendation.get('rationale', 'N/A')[:200]}...\n\nBenefit: The {suggested_pattern} pattern is better suited for your use case.")
        elif 'IMPROVE' in rec_type:
            print(f"\nRecommendation: Improve the {current_pattern} implementation\n\nReason: {recommendation.get('rationale', 'N/A')[:200]}...\n\nBenefit: Keep the pattern but fix implementation issues.")
        elif 'ADD' in rec_type:
            print(f"\nRecommendation: Add the {suggested_pattern} pattern\n\nReason: {recommendation.get('rationale', 'N/A')[:200]}...\n\nBenefit: This pattern would improve your code structure.")
        else:
            print(f"\nRecommendation: {rec_type}")
        
    def _parse_recommendation(self, response: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Parse recommendation response"""
        result = {
            'recommendation_type': 'NO_CHANGE',
            'current_pattern': analysis.get('current_pattern', 'None'),
            'suggested_pattern': 'None',
            'confidence': 0.5,
            'rationale': '', 'benefits': '',
            'should_modify': False
        }
        
        lines = response.strip().split('\n')
        current_field = None
        content = []
        
        # Parse lines
        for line in lines:
            line_upper = line.strip().upper()
            
            if line_upper.startswith('RECOMMENDATION:'):
                if current_field:
                    result[current_field] = '\n'.join(content).strip()
                rec_type = line.split(':', 1)[1].strip().upper()
                result['recommendation_type'] = rec_type
                result['should_modify'] = 'NO_CHANGE' not in rec_type and 'KEEP' not in rec_type
                current_field = None
                content = []
            elif line_upper.startswith('PATTERN:'):
                result['suggested_pattern'] = line.split(':', 1)[1].strip()
            elif line_upper.startswith('CONFIDENCE:'):
                try:
                    result['confidence'] = float(line.split(':', 1)[1].strip())
                except ValueError:
                    pass
            elif line_upper.startswith('RATIONALE:'):
                if current_field:
                    result[current_field] = '\n'.join(content).strip()
                current_field = 'rationale'
                content = []
            elif line_upper.startswith('BENEFITS:'):
                if current_field:
                    result[current_field] = '\n'.join(content).strip()
                current_field = 'benefits'
                content = []
            elif current_field and line.strip():
                content.append(line.strip())
        
        if current_field and content:
            result[current_field] = '\n'.join(content).strip()
        
        return result   
