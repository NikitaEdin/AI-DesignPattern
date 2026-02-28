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

# ----------------------
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

# ----------------------
# Retry logic tests for the CodeSnippetGenerator class
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
        code, is_valid, _ = generator.generate_code_snippet("Singleton", "E")

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
        """First generation returns code that fails evaluation, second generation returns code that passes - testing retry logic after evaluation failure"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [
            WRAPPED_SINGLETON_CODE,  # First generation: attempt returns code
            EVAL_FAIL_RESPONSE,      # First evaluation: fails
            WRAPPED_SINGLETON_CODE,  # Second generation: attempt returns code again
            EVAL_PASS_RESPONSE       # Second evaluation: passes
        ]
        generator = CodeSnippetGenerator(mock_llm, max_retries=2)
        _, is_valid, _ = generator.generate_code_snippet("Singleton", "E")

        self.assertTrue(is_valid)
        self.assertEqual(4, mock_llm.generate_response.call_count)


# ----------------------
# Feedback content
class TestFeedbackContent(unittest.TestCase):
    """ Test the content of feedback messages returned by the CodeGenerator """
    def test_pass_feedback_is_returned(self):
        """Feeedback from a PASS evaluation is correctly returned in the final feedback message"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_PASS_RESPONSE]

        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        _, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")

        self.assertTrue(is_valid)
        self.assertIn("Correctly implements", feedback)

    def test_fail_feedback_is_returned(self):
        """Feedback from a FAIL evaluation is correct returned"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_FAIL_RESPONSE]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        _, is_valid, feedback = generator.generate_code_snippet("Singleton", "E")

        self.assertFalse(is_valid)
        self.assertIn("Fails to properly implement", feedback)


# -----------
# Different patterns and difficulties
class TestPatternsAndDifficulties(unittest.TestCase):
    """Test code generation for different design patterns and difficulty levels"""

    def test_observer_pattern_easy(self):
        """Test code generation for the Observer pattern at Easy difficulty level"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_OBSERVER_CODE, EVAL_PASS_RESPONSE]

        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        code, is_valid, _ = generator.generate_code_snippet("Observer", "E")

        self.assertTrue(is_valid)
        self.assertIn("EventSystem", code)
        self.assertGreater(len(code), 0)
        self.assertEqual(2, mock_llm.generate_response.call_count)

    def test_hard_difficulty_pattern(self):
        """Verify difficult parameter influcences the prompt sent to LLM"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_OBSERVER_CODE, EVAL_PASS_RESPONSE]

        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        generator.generate_code_snippet("Singleton", "H")

        # get actual prompt sent to LLM on first attempt
        first_call_args = mock_llm.generate_response.call_args_list[0]
        prompt_text = str(first_call_args)
        # difficulty token should appear prompt
        self.assertIn("Difficulty Level: H", prompt_text)

# -----------
# Return-value testing
class TestReturnValueContract(unittest.TestCase):
    """Validate generate_code_snippet returns 3-tuple (code, is_valid, feedback)"""

    def _assert_tuple_contract(self, result):
        """Util method to assert return value of generate_code_snippet"""
        self.assertIsInstance(result, tuple)
        self.assertEqual(3, len(result))
        code, is_valid, feedback = result
        self.assertIsInstance(code, str)
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(feedback, str)

    def test_contract_on_success(self):
        """Test return value on successful gen and eval"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_PASS_RESPONSE]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        self._assert_tuple_contract(generator.generate_code_snippet("Singleton", "E"))

    def test_contract_on_eval_failure(self):
        """Test return value on generated code that fails evaluation"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_FAIL_RESPONSE]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        self._assert_tuple_contract(generator.generate_code_snippet("Singleton", "E"))

    def test_contract_on_no_code(self):
        """Test return value when generation fails to produce code, resulting in a failure response"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.return_value = ""
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        self._assert_tuple_contract(generator.generate_code_snippet("Singleton", "E"))


# -----------
# Edge-case inputs

class TestEdgeCaseInputs(unittest.TestCase):
    """Stress generator with unusual but plausible inputs"""

    def test_empty_pattern_string(self):
        """Test generator with empty pattern - should not raise and should default to Singleton pattern"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.return_value = ""
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        try:
            _, _, _ = generator.generate_code_snippet("", "E")
        except Exception as exc:
            self.fail(f"generate_code_snippet raised unexpectedly with empty pattern: {exc}")

    def test_unknown_difficulty_level(self):
        """Test generator with unknown difficulty - should not raise and should default to medium"""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [WRAPPED_SINGLETON_CODE, EVAL_PASS_RESPONSE]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        try:
            _, _, feedback = generator.generate_code_snippet("Singleton", "UNKNOWN")
        except Exception as exc:
            self.fail(f"generate_code_snippet raised unexpectedly with unknown difficulty: {exc}")

    def test_malformed_eval_response_treated_as_failure(self):
        """Test response with no PASS/FAIL keyword - should default to is_valid=False."""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [
            WRAPPED_SINGLETON_CODE,
            "Some void text without a verdict.",
        ]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        _, is_valid, _ = generator.generate_code_snippet("Singleton", "E")
        self.assertFalse(is_valid)

    def test_code_without_markdown_fences(self):
        """Raw Python code (no ``` fences) – behaviour should be consistent (no crash)."""
        mock_llm = _mock_llm()
        mock_llm.generate_response.side_effect = [
            SINGLETON_CODE,  # raw without code fences
            EVAL_PASS_RESPONSE,
        ]
        generator = CodeSnippetGenerator(mock_llm, max_retries=1)
        try:
            _, _, _ = generator.generate_code_snippet("Singleton", "E")
        except Exception as exc:
            self.fail(f"generate_code_snippet raised with fence-less code: {exc}")



if __name__ == "__main__":
    unittest.main()


