from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from catalogue import DIFFICULTY_LEVELS, WorkflowType
from file_manager import CodeSnippet

from shared.llm_interface import LLMInterface

# Analysis Result Class
#TODO: convert to TypedDict for performance. Having a class just to hold data is inefficient.

@dataclass
class AnalysisResult:
    """Results of analysing a code snippet"""
    snippet_path: str
    identified_pattern: str
    confidence: float
    explanation: str
    evaluation_pass: bool
    evaluation_feedback: str
    analysis_time: float
    expected_pattern: str = None
    difficulty: str = DIFFICULTY_LEVELS[0] # default to 'E'
    error: str = None
    workflow_type: WorkflowType = WorkflowType.SINGLE_PROMPT
    metadata: dict[str, Any] = None
    analysis_started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            'snippet_path': self.snippet_path,
            'identified_pattern': self.identified_pattern,
            'confidence': self.confidence,
            'explanation': self.explanation,
            'evaluation_pass': self.evaluation_pass,
            'evaluation_feedback': self.evaluation_feedback,
            'analysis_time': self.analysis_time,
            'expected_pattern': self.expected_pattern,
            'difficulty': self.difficulty,
            'error': self.error,
            'workflow_type': self.workflow_type,
            'metadata': self.metadata,
            'analysis_started_at': self.analysis_started_at
        }
        
	
class WorkflowInterface(ABC):
	
    def __init__(self, llm_interface: LLMInterface):
        self.llm_interface = llm_interface
        self.workflow_name = self.__class__.__name__
    
    @abstractmethod
    def execute(self, snippets: list[CodeSnippet]) -> list[AnalysisResult]:
        """
        Execute workflow with given list of code snippets

        Args:
        snippets: List of code snippets to analyse
        Returns:
        List of analysis results
        """


    def validate_snippets(self, snippets: list[CodeSnippet]) -> bool:
        """
        Validate snippets before processing
        """

        if not snippets:
            print("Error: no code snippets provided")
            return False
        
        for snippet in snippets:
            if not snippet.content or not snippet.content.strip():
                print(f"Warning: empty content in {snippet.filepath}")
        
        return True

    ### Getters
    @abstractmethod
    def get_workflow_type(self) -> WorkflowType:
        pass

    @abstractmethod
    def get_workflow_description(self) -> str:
        """
        Description of what this workflow does
        """


    ### Result generators
    def create_error_result(self, snippet: CodeSnippet, error: str, analysis_time: float = 0) -> AnalysisResult:
        """Create an error-ed result"""

        return AnalysisResult(
             snippet_path=snippet.filepath,
             identified_pattern='Error',
             confidence=0.0,
             explanation="Analysis failed due to error",
             evaluation_pass=False,
             evaluation_feedback="Not evaluated due to error",
             analysis_time=analysis_time,
             expected_pattern=snippet.design_pattern,
             difficulty=snippet.difficulty,
             error=error,
             workflow_type=self.get_workflow_type()
        )

    def create_success_result(self, snippet: CodeSnippet, analysis_data: dict[str, Any], analysis_time: float = 0) -> AnalysisResult:
        """Create AnalysisResult for successful analysis"""

        return AnalysisResult(
           snippet_path=snippet.filepath,
            identified_pattern=analysis_data.get('identified_pattern', 'Unknown'),
            confidence=analysis_data.get('confidence', 0.0),
            explanation=analysis_data.get('explanation', ''),
            evaluation_pass=analysis_data.get('evaluation_pass', False),
            evaluation_feedback=analysis_data.get('evaluation_feedback', ''),
            analysis_time=analysis_time,
            expected_pattern=snippet.design_pattern,
            difficulty=snippet.difficulty,
            error=None,
            workflow_type=self.get_workflow_type(),
            metadata=analysis_data.get('metadata', {})
        )         



		
    
	
	