""" Summarise CodeSnippet Data - Total snippets, by LLM and by pattern """

import os
from collections import defaultdict

CODE_SNIPPETS_DIR = "./CodeSnippets"  

def gather_stats(directory):
    total_count = 0
    llm_count = defaultdict(int)
    pattern_count = defaultdict(int)

    for pattern in os.listdir(directory):
        pattern_path = os.path.join(directory, pattern)
        if os.path.isdir(pattern_path):
            for filename in os.listdir(pattern_path):
                if filename.endswith(".py"):
                    parts = filename[:-3].split("_")
                    if len(parts) >= 4:
                        llm = parts[3].upper()
                        llm_count[llm] += 1
                        pattern_count[pattern] += 1
                        total_count += 1

    return total_count, llm_count, pattern_count

def print_stats(total, llm_count, pattern_count):
    # Total
    print(f"Total code snippets: {total}\n")
    
    # Per LLM prefix
    print("Snippets per LLM:")
    for llm, count in llm_count.items():
        print(f"  {llm}: {count}")
    print()
    
    # Per pattern
    print("Snippets per design pattern:")
    for pattern, count in pattern_count.items():
        print(f"  {pattern}: {count}")

if __name__ == "__main__":
    total, llm_count, pattern_count = gather_stats(CODE_SNIPPETS_DIR)
    print_stats(total, llm_count, pattern_count)
