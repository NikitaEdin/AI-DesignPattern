![Research](https://img.shields.io/badge/Research-Honours%20Project-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)


# LLM Efficiency in Code Design Pattern Identification
Honours research conducted by Nikita Lanetsky at Edinburgh Napier University.<br>
AI-driven static analysis for design pattern recognition, emphasising the the latest state of LLM and their efficiency.

> [!NOTE]  
Project setup and usage details will be shared upon completion, as the project is undergoing frequent updates and modifications.

---
- [Introduction](#introduction)
  - [Abstract](#abstract)
  - [Research Objectives](#research-objectives)
- [Methodology/Research Setup](#methodologyresearch-setup)
  - [Design Patterns Under Investigation](#design-patterns-under-investigation)
  - [Chosen LLMs/models](#chosen-llmsmodels)
  - [Programming Languages](#programming-languages)


## Introduction
### Abstract
This Honours project researches the ability and efficiency of the current state of Large Language Models (LLMs) in identifying implemented design patterns within source code.<br>
The research aims to evaluate four prominent top-leading LLM platforms - Ollama, OpenAI, Claude, and the recent rise of Kimi K2 - Through systemic testing using algorithmically generated and evaluated code samples containing various level of complexity in code and design patterns.

> [!NOTE]
> **Researcher Qualifications**: Anthropic Certified in Agentic AI & NVIDIA Certified in RAG Agents with LLMs

### Research Objectives
 **Primary Objective**:
- Quantify and compare the accuracy and efficiency of different LLMs in recognising common software design patterns in code implementations.
hosen LLM/Model
**Secondary Objectives**: 
- Analyse pattern recognition performance across different code complexities.
- Evaluate the impact of single and multi-layered algorithems on identification accuracy.
- Develop benchmarking methodologies for LLM code analysis capabilities.

## Methodology/Research Setup

### Design Patterns Under Investigation
13 Patterns in total.

- **Creational Patterns**: Singleton, Factory, Builder, Prototype.
- **Structural Patterns**: Adapter, Decorator, Facade, Proxy.
- **Behavioural Patterns**: Observer, Strategy, Command, Iterator, State.


### Chosen LLMs/Models
As of Q4 2025, the best LLMs for code generation and analysis are [Claude](https://claude.ai/) by [Anthropic](https://www.anthropic.com/), [Kimi K2](https://kimik2.com/) by [Moonshot](https://www.moonshot.ai/) and [ChatGPT](https://chatgpt.com/) by [OpenAI](https://openai.com/).

For an offline, free of charge, locally run model - [Ollama](https://github.com/ollama/ollama) will be used for rapid testing of algorithm functionality.

### Programming Languages
The primary aim is to focus on `Python` and slowly expand towards other languages, such as `Java` and `C#`.

> [!IMPORTANT]  
> The study primarily focuses on Python implementations. If time permits, the research may expand to include Java and C# to assess language-specific performance variations.

