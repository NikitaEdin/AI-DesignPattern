# AI-DesignPattern - Documentation Index

This folder contains detailed technical documentation for each project component. Use this guide to locate the relevant module based on your objective.

## Architecture Overview

The project evaluates LLM efficacy in design pattern recognition through three interconnected pillars:

1. **Code Generation** — Automated synthesis and LLM-based evaluation of design pattern implementations.
2. **Code Dataset** — Curated corpus of validated Python snippets across 13 GoF patterns and three complexity levels.
3. **Pattern Recognition** — LLM-driven static analysis to detect and identify embedded patterns.

All modules share a common LLM interface (`shared/llm_interface.py`) supporting multiple providers (OpenAI, Anthropic, xAI, Moonshot).

## Module Guide

| Topic | Description | Link |
|-------|-------------|------|
| **CodeGenerator** | AI code generation/evaluation for design patterns (CLI, CodeEvaluator class, usage). | [CodeGenerator.md](./CodeGenerator.md) |
| **CodeSnippets** | Dataset of 1500+ generated snippets (`<Pattern>_<ID>_<Difficulty>_<LLM>.py`), structure/naming. | [CodeSnippets.md](./CodeSnippets.md) |
| **PatternRecogniser** | Analyses snippets for pattern identification (workflows, CLI, reports). | [PatternRecogniser.md](./PatternRecogniser.md) |
| **PatternRecommender** | Recommends/refactors patterns (InteractiveWorkflow, CLI `pattern_recommender.py <file> <llm>`). | [PatternRecommender.md](./PatternRecommender.md) |


## Quick Reference

### CodeGenerator
- **Purpose**: LLM-driven code generation with automated evaluation
- **Entry Point**: `CodeGenerator/main_CG.py`

### PatternRecogniser
- **Purpose**: Analyse snippets to identify design patterns
- **Entry Point**: `PatternRecogniser/cli.py`

### PatternRecommender
- **Purpose**: Suggest refactoring to align code with design patterns
- **Entry Point**: `PatternRecommender/cli.py` or `pattern_recommender.py`

## Getting Started

1. **Generate snippets**: `python CodeGenerator/main_CG.py --pattern Singleton --difficulty E --llm claude --count 5`
2. **Recognise patterns**: `python PatternRecogniser/cli.py --llm claude --filter-pattern Factory`
3. **Recommend improvements**: `python PatternRecommender/cli.py --input your_code.py --llm openai`

Consult individual module documentation for advanced usage and API details.

For a high-level project overview, see the root [README.md](../README.md).
