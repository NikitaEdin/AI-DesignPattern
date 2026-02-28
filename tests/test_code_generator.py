import sys
import os
# Repo root & CodeGenerator directory added to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../CodeGenerator')))

import unittest
from unittest.mock import MagicMock

from CodeGenerator.code_generator import CodeSnippetGenerator


class TestCodeSnippetGenerator(unittest.TestCase):
    """Unit tests for the CodeSnippetGenerator class, focusing on code generation and evaluation logic"""
    VALID_CODE = """
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_value(self):
        return "shared value"

if __name__ == "__main__":
    cm1 = ConfigManager()
    cm2 = ConfigManager()
    print(cm1 is cm2)
    print(cm1.get_value())
"""

    EVAL_PASS_RESPONSE = """
    EVALUATION: PASS
    FEEDBACK: Correctly implements the Singleton pattern with proper instance control via __new__. Minimal implementation suitable for easy difficulty. Executable main section present. No naming violations."""

    EVAL_FAIL_RESPONSE = """
    EVALUATION: FAIL
    FEEDBACK: Fails to properly implement the pattern. Missing key components."""

    NO_CODE_RESPONSE = ""

    def test_generate_success(self):
        """Test successful code generation and evaluation for a valid Singleton implementation"""
        mock_llm = MagicMock()
        mock_llm.get_prefix.return_value = "TEST"
        code_response = f"""```python{self.VALID_CODE}```"""
        # Return valid code on first call, then a PASS evaluation response on second call
        mock_llm.generate_response.side_effect = [code_response, self.EVAL_PASS_RESPONSE]

        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")
        # Assertions
        self.assertTrue(is_valid)
        self.assertIn("ConfigManager", code)
        self.assertGreater(len(code), 0)
        self.assertEqual(2, mock_llm.generate_response.call_count)


    def test_generate_evaluation_failure(self):
        """Test code generation that produces code which fails evaluation due to missing components"""
        mock_llm = MagicMock()
        mock_llm.get_prefix.return_value = "TEST"
        code_response = f"""```python{self.VALID_CODE}```"""
        mock_llm.generate_response.side_effect = [code_response, self.EVAL_FAIL_RESPONSE]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")
        self.assertFalse(is_valid)
        self.assertIn("Missing key components", feedback)
        self.assertEqual(2, mock_llm.generate_response.call_count)


    def test_generate_no_valid_code(self):
        """Test code generation that fails to produce any valid code, resulting in retries and eventual failure"""
        mock_llm = MagicMock()
        mock_llm.generate_response.return_value = self.NO_CODE_RESPONSE
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")
        self.assertFalse(is_valid)
        self.assertEqual("", code)
        self.assertIn("Failed to generate a valid Python code snippet", feedback)
        self.assertEqual(1, mock_llm.generate_response.call_count)


if __name__ == "__main__":
    unittest.main()


