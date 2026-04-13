# PatternRecogniser (Third Pillar) Module Documentation

> [!NOTE]  
>  This documentation was AI-generated using grok-4.1.fast on 22-02-2026. Analysis included listing folder structure recursively, reading and analysing all Python scripts (add_shared.py, pattern_recogniser.py, catalogue.py, cli.py, file_manager.py, single_workflow.py, workflow_interface.py, report_generator.py), reviewing non-code outputs, and verifying architecture/data flow.
> All content has been manually verified, evaluated, and fixed for accuracy with the actual project.

## Overview

**PatternRecogniser** is an AI-powered tool that analyses Python code snippets to identify implemented GoF design patterns using LLMs (Grok, OpenAI, Claude, KimiK2). It supports filtering snippets by pattern, difficulty, generating LLM; custom inputs; single/multi workflows; and generates detailed reports (Excel, TXT).

Key goals:
- Test LLM ability to recognise design patterns in anonymised code (no pattern names leaked).
- Benchmark accuracy/confidence across LLMs, difficulties, workflows.
- Accumulate metrics in Excel for analysis/charts.

**Entry Point**: `python PatternRecogniser/pattern_recogniser.py [args]`

## Folder Structure

```
PatternRecogniser/
├── add_shared.py              # Adds project root to sys.path
├── pattern_recogniser.py       # Main CLI app
├── catalogue.py               # Constants (patterns, LLMs), filename parsers
├── cli.py                     # Arg parser/validation
├── file_manager.py            # Loads CodeSnippets/ or custom files
├── single_workflow.py         # Single-prompt workflow (identify + evaluate)
├── workflow_interface.py      # ABC + AnalysisResult dataclass
├── report_generator.py        # Excel/TXT reports
├── Input/                     # Custom inputs (e.g., facade.py - Facade example)
├── Output/                    # Custom results (e.g., facade_result.txt)
├── Analysis/                  # JSON outputs(analysis_claude.json)
├── Reports/                   # Excel reports (report_claude.xlsx)
└── Charts/                    # Visualisations (chart_claude.png)
```

## Architecture & Components

### 1. **CLI (cli.py)**
- Parses args: `--llm claude --filter-pattern Singleton --filter-difficulty M --count 5 --workflow single --input myfile.py`
- Validates: Patterns (`DESIGN_PATTERNS`: 13 total), Difficulties (`E/M/H`), LLMs (`ollama/openai/claude/kimi/grok/qwen`).
- Custom input overrides filters.

### 2. **FileManager (file_manager.py)**
- `locate_snippets(...)`: Regex-matches `CodeSnippets/<Pattern>/<Pattern>_<id>_<diff>_<llm_prefix>.py` (e.g., `Singleton_0_E_C.py` where `C=Claude`).
- `locate_custom_snippet(...)`: Loads from `Input/`.
- Returns `CodeSnippet` dataclass (filepath, content, metadata).

### 3. **Workflows**
- **Interface (workflow_interface.py)**: ABC with `execute(snippets) -> List[AnalysisResult]`.
- **SingleWorkflow (single_workflow.py)**:
  - Two-stage: 1) Identify pattern/confidence/explanation. 2) Evaluate identification quality (PASS/FAIL).
  - Retries (max=3) on eval fail.
  - Prompts: Strict format (PATTERN:/CONFIDENCE:/EXPLANATION:; EVALUATION:/FEEDBACK:).
  - Parsing robust with fallbacks.

### 4. **Main App (pattern_recogniser.py)**
```
CLI args → Validate → Locate snippets → LLM init → Workflow.execute() → ReportGenerator.save()
```

### 5. **Reporting (report_generator.py)**
- **Dataset mode**: Appends to `Reports/report_<analysing_llm>.xlsx` (cols: Date, Analysing_LLM, Generated_LLM, Snippet, Identified, Confidence, Success, Time, Workflow, Difficulty).
- **Custom mode**: `Output/<input>_result.txt` (detailed: pattern, conf, explanation, eval).
- Success: identified == expected (case-insensitive).

### 6. **Catalogue (catalogue.py)**
- Constants: `DESIGN_PATTERNS`, `DIFFICULTY_LEVELS`, `LLM_PROVIDERS`, `LLM_SHORT_MAP` (e.g., `C: claude`).
- Utils: `parse_filename(...)`, `is_file_generated_by_llm(...)`, `get_llm_prefix(...)`.

## Data Flow

```
CodeSnippets/ → FileManager (filter) → Workflow (LLM identify + eval w/ retries) → AnalysisResult[] → ReportGenerator → Reports/Output/
```

## Usage Examples

```bash
# Analyse all Singleton (M, Claude-generated) w/ Grok
python PatternRecogniser/pattern_recogniser.py --llm grok --filter-pattern Singleton --filter-difficulty M --filter-llm claude

# Custom file (Facade example)
python PatternRecogniser/pattern_recogniser.py --llm claude --input facade.py

# Top 10 Hard Factory w/ Grok
python PatternRecogniser/pattern_recogniser.py --llm grok --filter-pattern Factory --filter-difficulty H --count 10
```

**Output Example** (custom):
```
Identified Pattern: Facade
Confidence: 95%
Explanation: OS delegates to subsystems (FileServer, ProcessServer)...
Evaluation Pass: YES
```

## Key Features
- **Filtering**: Pattern/difficulty/LLM/count.
- **Retries**: Up to 3 on eval fail.
- **Benchmarking**: Success rate, time, confidence per LLM/difficulty.
- **Custom Support**: Any .py input.
- **Append Reports**: Cumulative Excel tracking.
- **Strict Prompts/Parsing**: Reliable LLM responses.

## Dependencies
- `shared/llm_interface.py` (LLMFactory).
- `pandas`, `openpyxl` (Excel).
- CodeSnippets/ (input dataset).

## Outputs & Analysis
- **Excel**: `Reports/report_claude.xlsx` → Charts (e.g., accuracy by difficulty).
- **TXT**: Detailed per-file.
- **JSON/Charts**: analysis_claude.json, chart_claude.png (post-processing).
