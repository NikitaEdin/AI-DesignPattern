import sys
import os
import re
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
CODE_SNIPPETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'CodeSnippets')

EXPECTED_PATTERNS = [
    "Adapter", "Builder", "Command", "Decorator", "Facade",
    "Factory", "Iterator", "Observer", "Prototype", "Proxy",
    "Singleton", "State", "Strategy"
]

# File structure
FILE_PATTERN = re.compile(r'^([A-Za-z]+)_(\d+)_(E|M|H)_([A-Za-z0-9]+)\.py$')

# Core expected parameters
EXPECTED_LLMS = {"C", "O", "GROK4F", "KimiK2"}
FILES_PER_DIFF = 10

class TestCodeSnippetsStructure(unittest.TestCase):
    """Tests CodeSnippets folder and file structure"""

    # Debug flag for additional prints
    DEBUG = False

    def test_files_follow_naming_pattern(self):
        """Verify files follow Pattern_Index_Difficulty_LLM.py format"""
        for pattern in EXPECTED_PATTERNS:
            pattern_path = os.path.join(CODE_SNIPPETS_DIR, pattern)
            if not os.path.exists(pattern_path):
                continue

            files = [f for f in os.listdir(pattern_path)
                     if os.path.isfile(os.path.join(pattern_path, f))]

            for file in files:
                match = FILE_PATTERN.match(file)
                self.assertIsNotNone(match, f"File '{file}' in '{pattern}' does not match naming pattern")

    def test_filename_matches_folder(self):
        """Verify pattern name matches parent folder"""
        for pattern in EXPECTED_PATTERNS:
            pattern_path = os.path.join(CODE_SNIPPETS_DIR, pattern)
            if not os.path.exists(pattern_path):
                continue

            files = [f for f in os.listdir(pattern_path)
                     if os.path.isfile(os.path.join(pattern_path, f))]

            for file in files:
                match = FILE_PATTERN.match(file)
                if match:
                    file_pattern = match.group(1)
                    self.assertEqual(file_pattern, pattern, f"Filename pattern '{file_pattern}' does not match folder '{pattern}'")

    
    def test_no_extra_files(self):
        """Verify only .py files exist in code snippets"""
        for pattern in EXPECTED_PATTERNS:
            pattern_path = os.path.join(CODE_SNIPPETS_DIR, pattern)
            if not os.path.exists(pattern_path):
                continue

            items = os.listdir(pattern_path)
            for item in items:
                item_path = os.path.join(pattern_path, item)
                if os.path.isfile(item_path):
                    self.assertTrue(item.endswith('.py'), f"Unexpected non-Python file '{item}' in '{pattern}'")

    def test_llm_and_difficulty_coverage(self):
        """Verify core params are counts met"""
        for pattern in EXPECTED_PATTERNS:
            pattern_path = os.path.join(CODE_SNIPPETS_DIR, pattern)
            if not os.path.exists(pattern_path):
                self.fail(f"Pattern folder '{pattern}' does not exist")

            files = [f for f in os.listdir(pattern_path) if f.endswith('.py')]

            llms_found = set()
            difficulties = {"E": 0, "M": 0, "H": 0}
            llm_counts = {llm: 0 for llm in EXPECTED_LLMS}
            unknown_llms = []
            non_matching = []

            # Loop through all files
            for file in files:
                match = FILE_PATTERN.match(file)
                if match:
                    diff = match.group(3)
                    llm = match.group(4)
                    difficulties[diff] += 1
                    if llm in EXPECTED_LLMS:
                        llms_found.add(llm)
                        llm_counts[llm] += 1
                    else:
                        unknown_llms.append(file)
                else:
                    non_matching.append(file)

            # Debug prints for missing files (internal only)
            if self.DEBUG:
                print(f"\n{pattern}: ", end="")
                counts_str = ", ".join([f"{llm}={llm_counts[llm]}" for llm in EXPECTED_LLMS])
                print(counts_str, end="")
                if unknown_llms:
                    print(f" - Unknown LLM: {unknown_llms}", end="")
                if non_matching:
                    print(f" - Invalid: {non_matching}", end="")
                print()

            missing_llms = EXPECTED_LLMS - llms_found
            self.assertEqual(
                missing_llms, set(),
                f"Pattern '{pattern}' missing LLMs: {missing_llms}"
            )

            for diff, count in difficulties.items():
                self.assertGreaterEqual(count, FILES_PER_DIFF, f"Pattern '{pattern}' has {count} '{diff}' files, expected at least {FILES_PER_DIFF}")


if __name__ == "__main__":
    unittest.main()
