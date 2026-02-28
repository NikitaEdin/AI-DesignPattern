import sys
import os
# Repo root & CodeGenerator directory added to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../CodeGenerator')))

import unittest
from unittest.mock import MagicMock, patch

from CodeGenerator.code_evaluator import CodeEvaluator

# -------------
# Shared
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

EVAL_PASS_RESPONSE = """
    EVALUATION: PASS
    FEEDBACK: Correctly implements the design pattern. Executable main section present. No naming violations."""

EVAL_FAIL_RESPONSE = """
    EVALUATION: FAIL
    FEEDBACK: Fails to properly implement the pattern. Missing key components."""

NO_CODE_RESPONSE = ""

def make_evaluator(response=None, side_effect=None):
    """Return mocked CodeEvaluator"""
    mock_llm = MagicMock()
    mock_llm.get_prefix.return_value = "TEST"
    if side_effect is not None: # Multiple calls with different responses
        mock_llm.generate_response.side_effect = side_effect
    elif response is not None: # Consistent response
        mock_llm.generate_response.return_value = response
    
    evaluator = CodeEvaluator(mock_llm)
    return evaluator, mock_llm


# -------------
# Return-value tests
class TestReturnValue(unittest.TestCase):
    """evaluate_code must always return (bool, str)"""

    def test_pass_returns_tuple(self):
        """Test PASS response returns (True, feedback)"""
        evaluator, _ = make_evaluator(response=EVAL_PASS_RESPONSE)
        result = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        is_valid, feedback = result
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(feedback, str)
        self.assertTrue(is_valid)


    def test_fail_path_returns_tuple(self):
        """Test FAIL response returns (False, feedback)"""
        evaluator, _ = make_evaluator(response=EVAL_FAIL_RESPONSE)
        result = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        is_valid, feedback = result
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(feedback, str)
        self.assertFalse(is_valid)

# -------------
# Correct evaluation verdicts
class TestEvaluationVerdicts(unittest.TestCase):
    """is_valid should reflect PASS/FAIL verdict in LLM response"""

    def test_pass_response(self):
        """EVALUATION: PASS, return is_valid=True"""
        evaluator, _ = make_evaluator(response=EVAL_PASS_RESPONSE)
        is_valid, feedback = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertTrue(is_valid)
        self.assertIn("Correctly implements the design pattern", feedback)

    def test_fail_response(self):
        """EVALUATION: FAIL, return is_valid=False"""
        evaluator, _ = make_evaluator(response=EVAL_FAIL_RESPONSE)
        is_valid, feedback = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertFalse(is_valid)
        self.assertGreater(len(feedback), 0)
        self.assertIn("Fails to properly implement the pattern", feedback)

# -------------
# Prompt construction
class TestPromptConstruction(unittest.TestCase):
    """Test prompt constructions for pattern name, difficulty, and code content"""

    # Helper to extract prompt passed to generate_response
    def _get_prompt(self, mock_llm):
        """Return string passed to generate_response"""
        return mock_llm.generate_response.call_args[0][0]

    def test_pattern_name_in_prompt(self):
        """Test design pattern name in prompt"""
        evaluator, mock_llm = make_evaluator(response=EVAL_PASS_RESPONSE)
        evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        prompt = self._get_prompt(mock_llm)
        self.assertIn("Singleton", prompt)

    def test_difficulty_in_prompt(self):
        """Test difficulty in prompt"""
        evaluator, mock_llm = make_evaluator(response=EVAL_PASS_RESPONSE)
        evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "H")
        prompt = self._get_prompt(mock_llm)
        self.assertIn("Expected Difficulty: Hard", prompt)

    def test_code_in_prompt(self):
        """Test code content in prompt"""
        evaluator, mock_llm = make_evaluator(response=EVAL_PASS_RESPONSE)
        evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        prompt = self._get_prompt(mock_llm)
        self.assertIn("class ConfigManager:", prompt)

    def test_different_patterns_produce_different_prompts(self):
        """Test different patterns produce different prompts"""
        evaluator, mock_llm = make_evaluator(response=EVAL_PASS_RESPONSE)
        evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        prompt_singleton = self._get_prompt(mock_llm)

        mock_llm.reset_mock() #Reset mock
        evaluator.evaluate_code("class Subject: pass", "Observer", "E")
        prompt_observer = self._get_prompt(mock_llm)

        self.assertNotEqual(prompt_singleton, prompt_observer)

# -------------
# Malformed LLM responses
class TestMalformedResponses(unittest.TestCase):
    """Test LLM response not following expected format- expected degrade rather than raise"""

    def test_empty_response_does_not_raise(self):
        """Empty response should not raise exception"""
        evaluator, _ = make_evaluator(response="")
        try:
            evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        except Exception as exc:
            self.fail(f"Empty LLM response raised: {exc}")

    def test_empty_response_returns_false(self):
        """Empty response should return is_valid=False"""
        evaluator, _ = make_evaluator(response="")
        is_valid, _ = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertFalse(is_valid)

    def test_no_verdict_keyword_returns_false(self):
        """Response with no PASS/FAIL default to invalid"""
        evaluator, _ = make_evaluator(response="The code looks okay I think.")
        is_valid, _ = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertFalse(is_valid)

    def test_response_with_only_feedback_no_verdict(self):
        """Response with feedback but no PASS/FAIL should return is_valid=False"""
        evaluator, _ = make_evaluator(response="FEEDBACK: Looks fine.")
        is_valid, _ = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertFalse(is_valid)

    def test_whitespace_only_response(self):
        """Response with whitespace should not raise and return is_valid=False"""
        evaluator, _ = make_evaluator(response="   \n\n  ")
        is_valid, _ = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertFalse(is_valid)

    def test_pass_in_wrong_position_not_misread(self):
        """PASS appearing in feedback should be misread as verdict"""
        response = "EVALUATION: FAIL\nFEEDBACK: Would pass if the pattern were complete."
        evaluator, _ = make_evaluator(response=response)
        is_valid, _ = evaluator.evaluate_code(SINGLETON_CODE, "Singleton", "E")
        self.assertFalse(is_valid)



if __name__ == "__main__":
    unittest.main()
