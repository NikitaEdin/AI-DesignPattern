"""
Interactive Workflow

Using conversational Agentic orchestration for pattern recommendation
"""

from typing import Dict, Any
from shared.llm_interface import LLMInterface
from workflow_interface import WorkflowInterface
from code_analyser import CodeAnalyser
class InteractiveWorkflow(WorkflowInterface):
    """
    Interactive conversational apporach

    Stages:
    1. Analyse code structure and patterns
    2. Conduct interactive conversation (to better understand)
    3. Generate recommendation
    4. Generated improved code (if approved)
    """

    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        
        # Init
        self.analyser = CodeAnalyser(llm_interface)


    def execute(self, code_snippet, filename):
        # Stage 1: Analyse code
        print(f'Stage 1: Analysing code...')
        analysis = self.analyser.analyse(code_snippet)
        self.analyser.display_analysis(analysis)


       
        return []

    def _handle_code_generation(
            self, original_code: str, 
            recommendation: Dict[str, Any], filename: str ) -> bool:
        """Handle code generation (+ user approval)"""

        if not recommendation.get('should_modify', False):
            print("Stage 4: No changes recommended")
            print("[Info] Code modification not approved by user. Skipping code generation.")
            recommendation['recommended_code'] = original_code
            return False
        
        # Display recommendation
        print("Stage 4: Recommendation Summary")
        self.recommendation_generation.display_recommendation(recommendation)

        # Request user approval for code generation
        if self.code_generator.request_user_approval():
            improved_code = self.code_generator.generate_improved_code(
                original_code, recommendation, filename
            )

            recommendation['recommended_code'] = improved_code
            return True
        else:
            recommendation['recommended_code'] = original_code
            return False


    def get_workflow_name(self):
        return "Interactive Workflow"
    
    def get_workflow_description(self):
        return "Interactive conversational agentic workflow, analysing, recommending and code generation."