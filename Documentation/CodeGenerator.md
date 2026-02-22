# CodeGenerator (First Pillar) Module Documentation

> [!NOTE]  
> This documentation was AI-generated using grok-4.1.fast on 22-02-2026. Analysis included reviewing the CodeGenerator folder contents (code_evaluator.py, main_CG.py), dependencies, class methods, usage examples (developer/CLI), and LLM integration.
> All content has been manually verified, evaluated, and fixed for accuracy with the actual project.

## Overview

The `CodeGenerator` folder contains tools for AI-assisted generation and evaluation of Python code snippets implementing design patterns (e.g., Singleton, Factory, Observer) at varying difficulty levels (Easy 'E', Medium 'M', Hard 'H').

Key components:
- `code_evaluator.py`: LLM-based evaluator for generated code.
- `main_CG.py`: CLI entrypoint for end-users to generate, evaluate, and save snippets to `CodeGenerationOutputs/`.

Uses LLM providers (OpenAI, Claude, Kimi) via `shared/llm_interface.py`.

## Dependencies

- `shared.llm_interface.LLMInterface` & `LLMFactory`
- `CodeGenerator.code_generator.CodeSnippetGenerator` (internal)
- `CodeGenerator.file_manager.FileManager` (internal)

## CodeEvaluator Class (code_evaluator.py)

### `__init__(self, llm: LLMInterface)`
Initialises with LLM instance.

### `evaluate_code(self, code: str, design_pattern: str, difficulty: str) -> Tuple[bool, str]`
Evaluates code against pattern/difficulty; returns (valid: bool, feedback: str).

### Private Methods
- `_create_evaluation_prompt(...)`: Strict criteria prompt (structure, components, syntax, quality, no naming leaks).
- `_parse_evaluation_response(...)`: Parses 'EVALUATION: PASS/FAIL' + 'FEEDBACK:'.
- `get_retry_prompt(original_prompt: str, feedback: str)`: Feedback-driven retry prompt.

## Key Features
- **Evaluation Criteria**: Pattern fidelity, completeness, runnable syntax, difficulty match, bug-free, no pattern names in code.
- **Difficulty Mapping**:
  | Level | Description |
  |-------|-------------|
  | E     | Basic core elements |
  | M     | Standard + features |
  | H     | Complex + optimisations/edges |
- **Robustness**: Exception handling, debug logging, format enforcement.

## Usage

### Developer Usage (Programmatic)
Load/evaluate code from files (no hardcoded snippets):

```python
from typing import Tuple
from shared.llm_interface import LLMInterface
from CodeGenerator.code_evaluator import CodeEvaluator

llm = LLMInterface(...)  # Your LLM setup
evaluator = CodeEvaluator(llm)

# Load from file
with open('path/to/generated_code.py', 'r') as f:
    code = f.read()

is_valid, feedback = evaluator.evaluate_code(code, 'Singleton', 'E')
print(f'Valid: {is_valid}\nFeedback: {feedback}')

# Retry if failed
if not is_valid:
    retry_prompt = evaluator.get_retry_prompt(original_prompt, feedback)
```

### CLI Usage (End-User via main_CG.py)
```bash
# Generate 3 Singleton snippets (Medium, grok)
python CodeGenerator/main_CG.py --pattern Singleton --count 3 --difficulty M --llm grok

# Factory (Hard, OpenAI)
python CodeGenerator/main_CG.py --pattern Factory --count 1 --difficulty H --llm openai
```
- Validates args, tests LLM connection.
- Generates/evaluates/saves to `CodeGenerationOutputs/` with metadata.
- Displays success rate, file list.

## Integration Notes
- For pipelines: Use `CodeSnippetGenerator` (wraps evaluator) in custom scripts.
- Outputs include timing, feedback; supports retries.
- Patterns: Singleton, Factory, Builder, etc. (14 total).

Refer to source files for details. This doc focuses on essentials.
