import sys
import os
# Repo root & CodeGenerator directory added to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../CodeGenerator')))

import unittest
from unittest.mock import MagicMock

from CodeGenerator.code_generator import CodeSnippetGenerator

def _mock_llm(prefix="TEST"):
    m = MagicMock()
    m.get_prefix.return_value = prefix
    return m


SINGLETON_CODE  = """
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

OBSERVER_CODE = """
class EventSystem:
    def __init__(self):
        self._listeners = []
    def subscribe(self, listener):
        self._listeners.append(listener)
    def notify(self, event):
        for listener in self._listeners:
            listener(event)
if __name__ == "__main__":
    es = EventSystem()
    es.subscribe(print)
    es.notify("hello")
"""

EVAL_PASS_RESPONSE = """
    EVALUATION: PASS
    FEEDBACK: Correctly implements the design pattern. Executable main section present. No naming violations."""

EVAL_FAIL_RESPONSE = """
    EVALUATION: FAIL
    FEEDBACK: Fails to properly implement the pattern. Missing key components."""

NO_CODE_RESPONSE = ""

WRAPPED_SINGLETON_CODE = f"```python{SINGLETON_CODE}```"
WRAPPED_OBSERVER_CODE = f"```python{OBSERVER_CODE}```"


# Unit tests for the CodeSnippetGenerator class, focusing on code generation and evaluation logic
class TestCodeSnippetGenerator(unittest.TestCase):
    """Unit tests for the CodeSnippetGenerator class, focusing on code generation and evaluation logic"""

    def test_generate_success(self):
        """Test successful code generation and evaluation for a valid Singleton implementation"""
        mock_llm = MagicMock()
        mock_llm.get_prefix.return_value = "TEST"
        # Return valid code on first call, then a PASS evaluation response on second call
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_PASS_RESPONSE]

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
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_FAIL_RESPONSE]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")
        self.assertFalse(is_valid)
        self.assertIn("Missing key components", feedback)
        self.assertEqual(2, mock_llm.generate_response.call_count)


    def test_generate_no_valid_code(self):
        """Test code generation that fails to produce any valid code, resulting in retries and eventual failure"""
        mock_llm = MagicMock()
        mock_llm.generate_response.return_value = NO_CODE_RESPONSE
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")
        self.assertFalse(is_valid)
        self.assertEqual("", code)
        self.assertIn("Failed to generate a valid Python code snippet", feedback)
        self.assertEqual(1, mock_llm.generate_response.call_count)

class TestRetryBehaviour(unittest.TestCase):
    """ Test the retry behaviour of the CodeGenerator """

    def test_retry_on_succeeds_on_second_attempt(self):
        """First generation call returns no code, second call returns valid code - testing retry logic and prompt adjustment"""
        mock_llm = _mock_llm()
        #  Attempt 1: empty response
        #  Attempt 2: valid code response
        mock_llm.generate_response.side_effect = [
            "",  # First attempt returns empty response
            WRAPPED_SINGLETON_CODE, 
            EVAL_PASS_RESPONSE  
        ]
        generator = CodeSnippetGenerator(mock_llm, max_retries=2)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")

        self.assertTrue(is_valid)
        self.assertIn("ConfigManager", code)


    def test_exhausted_retries_returns_failure(self):
        """All generation attempts return empty response - returning a failure after max attempts"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.return_value = ""  # Always return empty response

        max_retries = 3
        generator = CodeSnippetGenerator(mock_llm, max_retries=max_retries)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")

        self.assertFalse(is_valid)
        self.assertEqual("", code)
        self.assertIn("Failed to generate a valid Python code snippet", feedback)
        self.assertEqual(max_retries, mock_llm.generate_response.call_count)


    def test_retry_after_eval_fail(self):
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [
            WRAPPED_SINGLETON_CODE,  # First generation: attempt returns code
            EVAL_FAIL_RESPONSE,      # First evaluation: fails
            WRAPPED_SINGLETON_CODE,  # Second generation: attempt returns code again
            EVAL_PASS_RESPONSE       # Second evaluation: fails
        ]
        generator = CodeSnippetGenerator(mock_llm, max_retries=2)
        code, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")

        self.assertTrue(is_valid)
        self.assertEqual(4, mock_llm.generate_response.call_count)

if __name__ == "__main__":
    unittest.main()


