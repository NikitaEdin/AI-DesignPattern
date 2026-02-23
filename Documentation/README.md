# AI-DesignPattern Project Documentation

> [!NOTE]  
> Central index for module/subproject documentation. AI-generated using grok-4.1.fast on 22-02-2026; manually verified for accuracy.

## Introduction

This folder contains detailed guides for the AI-DesignPattern project's key components. Use the table below to find relevant documentation based on your needs:

| Topic | Description | Link |
|-------|-------------|------|
| **CodeGenerator** | AI code generation/evaluation for design patterns (CLI, CodeEvaluator class, usage). | [CodeGenerator.md](./CodeGenerator.md) |
| **CodeSnippets** | Dataset of 1500+ generated snippets (`<Pattern>_<ID>_<Difficulty>_<LLM>.py`), structure/naming. | [CodeSnippets.md](./CodeSnippets.md) |
| **PatternRecogniser** | Analyses snippets for pattern identification (workflows, CLI, reports). | [PatternRecogniser.md](./PatternRecogniser.md) |
| **PatternRecommender** | Recommends/refactors patterns (InteractiveWorkflow, CLI `pattern_recommender.py <file> <llm>`). | [PatternRecommender.md](./PatternRecommender.md) |

## Quick Guide

- **Generating code?** → CodeGenerator.md (CLI: `main_CG.py --pattern Singleton --llm ollama`).
- **Exploring dataset?** → CodeSnippets.md.
- **Benchmarking recognition?** → PatternRecogniser.md (`PatternRecogniser.py --llm claude --filter-pattern Factory`).
- **Refactoring code?** → PatternRecommender.md (`pattern_recommender.py codesnippet.py claude`).

See project root [README.md](../README.md) for high-level overview. All docs use UK spelling/EU dates; AI-assisted but verified.
