""" Generate a report of missing code snippets of different LLMs and suggest commands to generate them """

import os
from collections import defaultdict

CODE_SNIPPETS_DIR = "./CodeSnippets" 
EXPECTED_COUNT = 10
DIFFICULTIES = ["E", "M", "H"]

def check_snippets(directory):
    report = defaultdict(lambda: defaultdict(lambda: {d: 0 for d in DIFFICULTIES}))

    for pattern in os.listdir(directory):
        pattern_path = os.path.join(directory, pattern)
        if os.path.isdir(pattern_path):
            for filename in os.listdir(pattern_path):
                if filename.endswith(".py"):
                    parts = filename[:-3].split("_")
                    if len(parts) >= 4:
                        difficulty = parts[2].upper()
                        llm = parts[3].upper()
                        if difficulty in DIFFICULTIES:
                            report[pattern][llm][difficulty] += 1
    
    final_report = {}
    for pattern, llms in report.items():
        for llm, counts in llms.items():
            missing = {}
            for d in DIFFICULTIES:
                if counts[d] < EXPECTED_COUNT:
                    missing[d] = EXPECTED_COUNT - counts[d]
            if missing:
                if pattern not in final_report:
                    final_report[pattern] = {}
                final_report[pattern][llm] = missing

    return final_report

def generate_commands(report):
    """ Generate CLI commands to create missing snippets """
    commands = []
    for pattern, llms in report.items():
        for llm, missing in llms.items():
            for difficulty, count in missing.items():
                commands.append(
                    f"python main_CG.py --pattern {pattern} --count {count} --llm {llm.lower()} --difficulty {difficulty}"
                )
    return commands

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

if __name__ == "__main__":
    report = check_snippets(CODE_SNIPPETS_DIR)
    print_report(report)

    print("\nCommands to generate missing snippets:")
    commands = generate_commands(report)
    for cmd in commands:
        print(cmd)
