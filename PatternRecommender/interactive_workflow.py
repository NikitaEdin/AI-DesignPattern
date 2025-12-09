"""
Interactive Workflow

Using conversational Agentic orchestration for pattern recommendation
"""

from typing import Dict, Any
from shared.llm_interface import LLMInterface
from workflow_interface import WorkflowInterface
from code_analyser import CodeAnalyser
from conversation_manager import ConversationManager
from recommendation_generator import RecommendationGenerator
from code_generator import CodeGenerator

class InteractiveWorkflow(WorkflowInterface):
    """
    Interactive conversational apporach

    Phases:
    1. Analyse code structure and patterns
    2. Conduct interactive conversation (to better understand)
    3. Generate recommendation
    4. Generate improved code (if approved)
    """

    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        
        # Init
        self.analyser = CodeAnalyser(llm_interface)
        self.conversation_manager = ConversationManager(llm_interface)
        self.recommendation_generation = RecommendationGenerator(llm_interface)
        self.code_generator = CodeGenerator(llm_interface)


    def execute(self, code_snippet, filename):
        # Phase 1: Analyse code
        print(f"\nPhase 1: Analysing code...\n{'=' * 60}")

        analysis = self.analyser.analyse(code_snippet)
        self.analyser.display_analysis(analysis)


        # Phase 2: Interactive conversation
        print(f"\nPhase 2: Interactive conversation...\n{'=' * 60}")
        print("\nType your answers to help me understand your code better.\nType 'skip' to skip a question, or 'done' to finish early.\n")

        insights = self.conversation_manager.conduct_conversation(code_snippet, analysis)


        # Phase 3: Generation recommendation
        print(f"\nPhase 3: Generating recommendation...\n{'=' * 60}")
        recommendation = self.recommendation_generation.generate_recommendation(
            code_snippet, analysis, insights
        )
        
        # Phase 4: Generate code (if approved)
        code_generated = self._handle_code_generation(
            code_snippet, recommendation, filename
        )

        # Results
        recommendation['code_generated'] = code_generated
        return recommendation

    def _handle_code_generation(
            self, original_code: str, 
            recommendation: Dict[str, Any], filename: str ) -> bool:
        """Handle code generation (+ user approval)"""

        if not recommendation.get('should_modify', False):
            print("No changes recommended")
            print("[Info] Code modification not approved by user. Skipping code generation.")
            recommendation['recommended_code'] = original_code
            return False
        
        # Display recommendation
        self.recommendation_generation.display_recommendation_summary(recommendation)


        print(f"\nPhase 4: Generating code...\n{'=' * 60}")
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