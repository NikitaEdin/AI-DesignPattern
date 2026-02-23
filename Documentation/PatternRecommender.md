# PatternRecommender Subproject Documentation

> [!NOTE]  
> This documentation was AI-generated using grok-4.1.fast on 22-02-2026. Analysis included listing folder structure recursively, reviewing add_shared.py, Input/codesnippet_1.py (Singleton pull example), Output/codesnippet_1_result.py (Observer push refactor), and inferring purpose/architecture from examples. All content has been manually verified, evaluated, and fixed for accuracy with the actual project.

## Overview

PatternRecommender is an AI-powered module for analysing existing code snippets and recommending/refactoring them to use more appropriate design patterns. It identifies suboptimal implementations (e.g., misuse of Singleton for publisher-subscriber) and generates improved versions using better-suited patterns (e.g., Observer for push notifications).


**Key Benefits Demonstrated**:
- **Before (Input)**: Singleton + polling → Busy-waiting, no decoupling.
- **After (Output)**: Observer → Dynamic attach/detach, automatic notify, extensible subscribers.

## Folder Structure

```
PatternRecommender/
├── add_shared.py     # Adds project root to sys.path
├── CLI.py            # CLI arg parsing & file I/O
├── pattern_recommender.py # Main entrypoint
├── interactive_workflow.py # Coordinates workflow phases
├── workflow_interface.py  # Workflow ABC + dataclasses
├── code_analyser.py      # Code analysis & DPR
├── conversation_manager.py # Interactive Q&A
├── agent_prompts.py       # Prompt templates
├── recommendation_generator.py # Generates/parses recs
├── code_generator.py      # Improved code generation
├── Input/          # Input code snippets
└── Output/         # Output results/logs
```

## Example Verdict

**Input** (`codesnippet_1.py`): Singleton publisher with polling subscribers.
- **Issues**: Manual pulls inefficient; violates single responsibility; tight coupling.

**Output** (`codesnippet_1_result.py`): Observer implementation.
- **Verdict**: "Replaced pull with push; added ABC interfaces; loose coupling via attach/detach/notify."
- **Demo**: Publisher notifies multiple subscribers automatically; unsubscribe works.


## CLI Usage

**Entry Point**: `python PatternRecommender/pattern_recommender.py <filename> <llm>`

- `<filename>`: `.py` file in `Input/` (max 200 lines).
- `<llm>`: Provider (ollama/openai/claude/grok/etc.).

**Examples** (from epilog):
```bash
python PatternRecommender/pattern_recommender.py codesnippet_1.py openai
python PatternRecommender/pattern_recommender.py code_snippet1.py kimi
python PatternRecommender/pattern_recommender.py code.py claude
```

**Flow**:
1. Validates/reads Input/<file>.py.
2. Inits LLM.
3. Runs InteractiveWorkflow: Analyse → Conversation (up to 5 Q&A) → Recommend → User approve → Generate code/log.
4. Saves Output/<file>_result.py (refactored code), <file>_log.txt.

**Output Example**: codesnippet_1_result.py (Singleton polling → Observer push).

## Extending with New Workflows

Currently uses `InteractiveWorkflow` (analyse → converse → recommend → generate w/ approval).

**To Add New**:
1. Implement `WorkflowInterface` subclass:
   ```python
   class NewWorkflow(WorkflowInterface):
       def execute(self, code: str, filename: str) -> Dict[str, Any]:
           # Custom logic
           pass
       def get_workflow_name(self) -> str:
           return "NewWorkflow"
       def get_workflow_description(self) -> str:
           return "Description"
   ```
2. Register in `pattern_recommender.py` main (add arg `--workflow`, factory like LLMFactory).
3. Integrate phases: CodeAnalyser, ConversationManager, RecommendationGenerator, CodeGenerator.

Supports agentic extensibility (prompts in agent_prompts.py).

**Use Cases**:
- Code reviews: "This Singleton should be Observer."
- Legacy refactor: Auto-upgrade polling to pub-sub.
- Education: Pattern evolution examples.

## Dependencies
- `shared/llm_interface.py` (LLMFactory).
- `shared/` modules (prompts/utils).
