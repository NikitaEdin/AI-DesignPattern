"""
Workflow Interface

Base interface for all workflow implementations
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

# dataclass for Analysis results
@dataclass
class AnalysisResult:
    """Data class for code analysis results"""
    current_pattern: str
    confidence: float
    purpose: str
    issues: list
    strengths: list


# dataclass for Recommendation results
@dataclass
class RecommendationResult:
    """Data class for recommendation results"""
    recommendation_type: str
    current_pattern: str
    suggested_pattern: str
    confidence: float
    rationale: str
    benefits: str
    should_modify: bool
    recommended_code: Optional[str] = None
    code_generated: bool = False

# Workflow Interface
class WorkflowInterface(ABC):
    """Abstract base for workflows"""
    
    @abstractmethod
    def execute(self, code_snippet: str, filename: str) -> Dict[str, Any]:
        """
        Execute the workflow on given code snippet.
        
        Args:
            code_snippet: Python code to analyse
            filename: Name of the file being analysed
            
        Returns:
            Dictionary containing workflow results
        """
        pass
    
    @abstractmethod
    def get_workflow_name(self) -> str:
        """Return the name of this workflow"""
        pass
    
    @abstractmethod
    def get_workflow_description(self) -> str:
        """Return the description of this workflow"""
        pass
