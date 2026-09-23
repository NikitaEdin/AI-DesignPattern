from datetime import datetime, timezone
import time
from typing import Any, Dict, List
from catalogue import DESIGN_PATTERNS, WorkflowType
from file_manager import CodeSnippet
from workflow_interface import AnalysisResult, WorkflowInterface
from shared.llm_interface import LLMInterface


max_attempts = 3

class SingleWorkflow(WorkflowInterface):
    def __init__(self, llm_interface: LLMInterface,  max_retries: int = 3):
        super().__init__(llm_interface)
        self.max_retries = max_retries
        
    def get_workflow_type(self) -> WorkflowType:
        return WorkflowType.SINGLE_PROMPT
    
    def get_workflow_description(self) -> str:
        return "Analyse each code snippet through pattern identification and evaluation stages"
    

    def execute(self, snippets: List[CodeSnippet]) -> List[AnalysisResult]:
        """ Execute single workflow on given code snippets"""

        if not self.validate_snippets(snippets):
            return []
        
        # TODO: display workflow info

        results = []
        for i, snippet in enumerate(snippets, 1):
            print(f"[{i}/{len(snippets)}] Analysing: {snippet.filename}")
            
            # Track when started
            start_time = time.time()
            analysis_started_at = datetime.now(timezone.utc)

            # Analyse code snippet
            result = self._analyse_single_snippet(snippet)

            # Record time taken
            result.analysis_time = time.time() - start_time
            result.analysis_started_at = analysis_started_at

            # Print result
            print(f"  Identified: {result.identified_pattern} ({result.confidence})")
    
            # Append result
            results.append(result)

            # TODO: Display progress
        #TODO: display result summary
        return results
    

    def _analyse_single_snippet(self, snippet: CodeSnippet) -> AnalysisResult:
        """Analyse single code snippet suing two-stage process (identify and evaluate)"""
        start_time = time.time()
        last_error = None


        for attempt in range(max_attempts):
            try:
                # Pattern analysis
                analysis_data = self._analyse_pattern(snippet)
                if analysis_data.get('error'):
                    last_error = analysis_data['error']
                    continue # try again

                # Evaluation (verify correctness & confidence))
                evaluation_data = self._evaluate(snippet, analysis_data)

                # Evaluation pass? return result
                if evaluation_data.get('evaluation_pass', False):
                    # Combine results
                    combined_data = {**analysis_data, **evaluation_data}
                    analysis_time = time.time() - start_time
                    return self.create_success_result(snippet, combined_data, analysis_time)
                
                # Evaluation failed? retry
                if attempt < max_attempts - 1:
                    print(f"  Evaluation failed, retrying... (Attempt {attempt + 1}/{max_attempts})")
                    continue
                else:
                    # Last attempt failed - return result
                    combined_data = {**analysis_data, **evaluation_data}
                    analysis_time = time.time() - start_time
                    return self.create_success_result(snippet, combined_data, analysis_time)

            except Exception as e:
                last_error = f'Unexpected error during analysis: {str(e)}'
                print(f"Error: {last_error}")
                if attempt == max_attempts - 1:
                    analysis_time = time.time() - start_time
                    return None
                
        # All attempts failed - return error result
        analysis_time = time.time() - start_time
        return None


    def _analyse_pattern(self, snippet: CodeSnippet) -> Dict[str, Any]:
        try:
            analysis_data = self._get_analysis_data(snippet)
            if self.llm_interface.supports_typed_decisions():
                analysis_data = self._guard_empty_pattern(snippet, analysis_data)
                analysis_data = self._guard_known_pattern(snippet, analysis_data)
            return analysis_data
        except Exception as e:
            return {'error': f"Pattern analysis failed: {str(e)}"}


    def _get_analysis_data(self, snippet: CodeSnippet) -> Dict[str, Any]:
        if self.llm_interface.supports_typed_decisions():
            return self._analyse_pattern_typed(snippet)
        analysis_prompt = self._create_analysis_prompt(snippet.content)
        analysis_response = self.llm_interface.generate_response(analysis_prompt)
        return self._parse_analysis_response(analysis_response)


###################### GUARD RAILS ######################

    def _guard_empty_pattern(self, snippet: CodeSnippet, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure a non-empty pattern was identified - retry once, then default to the first available pattern."""
        if str(analysis_data.get('identified_pattern') or '').strip():
            return analysis_data

        print("  Warning: empty pattern identification, retrying...")
        analysis_data = self._get_analysis_data(snippet)
        if not str(analysis_data.get('identified_pattern') or '').strip():
            print(f"  Warning: still empty after retry, defaulting to '{DESIGN_PATTERNS[0]}'")
            analysis_data['identified_pattern'] = DESIGN_PATTERNS[0]

        return analysis_data


    def _guard_known_pattern(self, snippet: CodeSnippet, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure the identified pattern is one of the available patterns - retry once, then default to
        the first available pattern with 0 confidence."""
        if analysis_data.get('identified_pattern') in DESIGN_PATTERNS:
            return analysis_data

        print(f"  Warning: '{analysis_data.get('identified_pattern')}' is not a recognised pattern, retrying...")
        analysis_data = self._get_analysis_data(snippet)
        if analysis_data.get('identified_pattern') not in DESIGN_PATTERNS:
            print(f"  Warning: still unrecognised after retry, defaulting to '{DESIGN_PATTERNS[0]}' with 0 confidence")
            analysis_data['identified_pattern'] = DESIGN_PATTERNS[0]
            analysis_data['confidence'] = 0.0

        return analysis_data


    def _evaluate(self, snippet: CodeSnippet, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if self.llm_interface.supports_typed_decisions():
                return self._evaluate_typed(snippet, analysis_data)
            evaluation_prompt = self._create_evaluation_prompt(snippet.content, analysis_data)
            evaluation_response = self.llm_interface.generate_response(evaluation_prompt)
            return self._parse_evaluation_response(evaluation_response)
        except Exception as e:
            return{
                'evaluation_pass': False,
                'evaluation_feedback': f"Evaluation failed: {str(e)}"
            }


###################### TYPED DECISIONS (e.g. Jev) ######################

    def _analyse_pattern_typed(self, snippet: CodeSnippet) -> Dict[str, Any]:
        """Identify the design pattern by asking a typed 'choice' question over
        the available design patterns, instead of a free-text prompt."""
        criteria = {pattern: f"The code implements the {pattern} pattern" for pattern in DESIGN_PATTERNS}
        criteria["None"] = "No recognisable design pattern is implemented"

        questions = {
            "pattern": {
                "type": "choice",
                "instructions": "Which design pattern (if any) is implemented in this code?",
                "criteria": criteria
            }
        }

        answers = self.llm_interface.generate_decision(state=snippet.content, questions=questions)
        pattern_answer = answers["pattern"]
        identified_pattern = pattern_answer["choice"]
        confidence = pattern_answer.get("probabilities", {}).get(identified_pattern, 0.0)

        return {
            'identified_pattern': identified_pattern,
            'confidence': confidence,
            'explanation': self._format_decision_explanation(pattern_answer)
        }


    def _evaluate_typed(self, snippet: CodeSnippet, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify the identification by asking a typed yes/no ('noul') question."""
        identified_pattern = analysis_data.get('identified_pattern', 'Unknown')
        questions = {
            "is_correct": {
                "type": "noul",
                "instructions": f"The code was identified as implementing the '{identified_pattern}' pattern. "
                                 "Is this identification correct?"
            }
        }

        answers = self.llm_interface.generate_decision(state=snippet.content, questions=questions)
        confidence = answers["is_correct"]["noul"]

        return {
            'evaluation_pass': confidence >= 0.5,
            'evaluation_feedback': f"Jev confidence that the identification is correct: {confidence:.0%}"
        }


    def _format_decision_explanation(self, pattern_answer: Dict[str, Any]) -> str:
        probabilities = pattern_answer.get("probabilities", {})
        top = sorted(probabilities.items(), key=lambda kv: kv[1], reverse=True)[:3]
        ranked = ", ".join(f"{name} ({prob:.0%})" for name, prob in top)
        return f"Jev decision probabilities (no natural-language rationale available): {ranked}"


###################### PROMPTS ######################

    def _create_analysis_prompt(self, code_snippet:str) -> str:
        return f"""
TASK: Analyse the code snippet and identify which design pattern (if any) is implemented.

You're limited to these specific design patterns:
{", ".join(DESIGN_PATTERNS)}

Analyse the following code snippet and identify any design pattern it implements;

```
{code_snippet}
```

RESPONSE FORMAT:
PATTERN: [ONE pattern name or "None" if no clear pattern]
CONFIDENCE: [0.0 - 1.0]
EXPLANATION: [Brief and short explanation of your reasoning, including key indications that led to your identification]

Focus on:
1. The structural characteristics of the code
2. The relationships between classes/objects
3. The intent and purpose of the implementation
4. How it solves common design problems
"""


    def _create_evaluation_prompt(self, code_snippet: str, analysis_data: Dict[str, Any]) -> str:

        return f"""
You are a code reviewer specialising in design patterns. 
TASK: Evaluate the following Python code snippet and assess the quality and accuracy of a design pattern identification.

Original code:
```
{code_snippet}
```

Analysis Result:
- Pattern: {analysis_data.get('identified_pattern', 'Unknown')}
- Confidence: {analysis_data.get('confidence', 0.0)}
- Explanation: {analysis_data.get('explanation', 'No explanation provided')}

Consider the following criteria:
1. Correctness of pattern identification
2. Quality and clarity of explanation
3. Appropriate confidence level
4. Overall analysis quality
5. Identification of key pattern characteristics

RESPONSE FORMAT:
EVALUATION: [PASS/FAIL]
FEEDBACK: [Constructive feedback on the analysis, including what was done well and areas for improvement]
"""
    
###################### PROMPT PARSING ######################

    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:

        result = {
            'identified_pattern': 'Unknown',
            'confidence': 0.5,
            'explanation': response
        }

        try:
            lines = response.strip().split("\n")
            for i, line in enumerate(lines):
                if line.startswith('PATTERN:'):
                    result['identified_pattern'] = line.split(':', 1)[1].strip()
                elif line.startswith('CONFIDENCE:'):
                    try:
                        confidence_str = line.split(':', 1)[1].strip()
                        result['confidence'] = float(confidence_str)
                    except (ValueError):
                        pass
                elif line.startswith('EXPLANATION:'):
                    result['explanation'] = '\n'.join(lines[i:]).split(':', 1)[1].strip()
                    break  
        except Exception as e:
            result ["error"] = f"Failed to parse analysis response: {str(e)}"

        return result


    def _parse_evaluation_response(self, response: str) -> Dict[str, Any]:
        result = {
            'evaluation_pass': False,
            'evaluation_feedback': response
        }
        try:
            lines = response.strip().split('\n')

            for i, line in enumerate(lines):
                if line.lstrip().upper().startswith('EVALUATION:'):
                    result['evaluation_pass'] = line.split(":", 1)[1].strip().upper()
                elif line.lstrip().upper().startswith('FEEDBACK'):
                    result['evaluation_feedback'] = '\n'.join(lines[i:]).split(':', 1)[1].strip()
                    break
        except Exception as e:
            result['evaluation_feedback'] = f'Failed to parse evaluation response: {str(e)}'
        return result

            