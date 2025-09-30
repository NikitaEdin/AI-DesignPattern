""" Generate a report of missing code snippets of different LLMs """

import os
from collections import defaultdict


CODE_SNIPPETS_DIR = "../CodeSnippets" 
# Expected code snippet PER difficulty
EXPECTED_COUNT = 10

# Code complexity level, aka "difficulty"
DIFFICULTIES = ["E", "M", "H"]

# LLM prefixes to CLI argument names
LLM_MAPPING = {
    "O": "openai",
    "L": "ollama",
    "C": "claude",
    "GROK4F": "grok4fast",
    "KimiK2": "kimi"
}

def check_snippets(directory):
    # Report structure: 
    ## report[pattern]: auto-creates a defaultdict
    ## report[pattern][llm]: auto-creates a dict {d: 0 for d in DIFFICULTIES}
    report = defaultdict(lambda: defaultdict(lambda: {d: 0 for d in DIFFICULTIES}))

    # Loop through pattern folders
    for pattern in os.listdir(directory):
        pattern_path = os.path.join(directory, pattern)
        if os.path.isdir(pattern_path):
            for filename in os.listdir(pattern_path):
                if filename.endswith(".py"):
                    # remove .py (-3 of length)
                    parts = filename[:-3].split("_")  
                    # 4 parts (pattern, id, diff, llm)
                    if len(parts) >= 4:
                        difficulty = parts[2].upper()
                        llm = parts[3].upper()
                        if difficulty in DIFFICULTIES:
                            report[pattern][llm][difficulty] += 1
    
    # Report
    final_report = {}
    for pattern, llms in report.items():
        for llm, counts in llms.items():
            missing = {}
            # Track missing items
            for d in DIFFICULTIES:
                if counts[d] < EXPECTED_COUNT:
                    missing[d] = EXPECTED_COUNT - counts[d]

            # Display only missing items
            if missing: 
                if pattern not in final_report:
                    final_report[pattern] = {}
                final_report[pattern][llm] = missing
    
    return final_report

def print_report(report):
    if not report:
        print("All patterns and LLMs have complete snippets.")
        return
    
    for pattern, llms in report.items():
        print(f"Pattern: {pattern}")
        for llm, missing in llms.items():
            missing_str = ", ".join(f"{d}={count}" for d, count in missing.items())
            print(f"  LLM: {llm} -> Missing snippets: {missing_str}")
        print("-" * 50)

# Generate CLI commands for missing snippets 
def generate_commands(report):
    commands = []
    for pattern, llms in report.items():
        for llm, missing in llms.items():
            llm_cli = LLM_MAPPING.get(llm.upper(), llm.lower())
            for difficulty, count in missing.items():
                commands.append(
                    f"python main_CG.py --pattern {pattern} --count {count} --llm {llm_cli} --difficulty {difficulty}"
                )
    return commands

if __name__ == "__main__":
    report = check_snippets(CODE_SNIPPETS_DIR)
    print_report(report)

    commands = generate_commands(report)
    if commands:
        print("\nCommands to generate missing snippets:")
        for cmd in commands:
            print(cmd)
