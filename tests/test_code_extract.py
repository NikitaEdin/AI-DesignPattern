import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../CodeGenerator')))

import unittest
from unittest.mock import MagicMock
from CodeGenerator.code_generator import CodeSnippetGenerator


def make_generator() -> CodeSnippetGenerator:
    """Return CodeSnippetGenerator with mock LLM"""
    mock_llm = MagicMock()
    mock_llm.get_prefix.return_value = "TEST"
    return CodeSnippetGenerator(mock_llm, max_retries=1)


# util to shorten test code
def extract(response: str) -> str:
    return make_generator()._extract_python_code(response)


# -------------
# Fenced code blocks  (``` / ```python)
class TestFencedCodeBlocks(unittest.TestCase):
    """Responses contain markdown fencing"""

    def test_python_fenced_block_is_extracted(self):
        """Standard triple backticks with 'python' tag"""
        response = "```python\nprint('hello')\n```"
        self.assertEqual("print('hello')", extract(response))

    def test_generic_fenced_block_is_extracted(self):
        """Triple backticks without language tag"""
        response = "```\nprint('hello')\n```"
        self.assertEqual("print('hello')", extract(response))

    def test_fenced_block_strips_surrounding_whitespace(self):
        """Leading/trailing whitespace around code should be removed"""
        response = "```python\n   x = 1\n   y = 2\n```"
        result = extract(response)
        self.assertNotEqual(result[0], " ")   # leading whitespace removed
        self.assertNotEqual(result[-1], " ")  # trailing whitespace removed

    def test_multiline_fenced_block(self):
        """"Multiline code within fences"""
        code = "def foo():\n    return 117\n\nprint(foo())"
        response = f"```python\n{code}\n```"
        self.assertIn("def foo():", extract(response))
        self.assertIn("print(foo())", extract(response))

    def test_only_first_fenced_block_is_returned(self):
        """Multiple fenced blocks exist - only return first"""
        response = "```python\nfirst = 1\n```\n\n```python\nsecond = 2\n```"
        result = extract(response)
        self.assertIn("first", result)
        self.assertNotIn("second", result)

    def test_fenced_block_with_prose_before_and_after(self):
        """Comment text around block should be ignored"""
        response = (
            "Sure, here is the code:\n\n"
            "```python\nx = 117\n```\n\n"
            "Hope that helps!"
        )
        self.assertEqual("x = 117", extract(response))

    def test_fenced_block_with_leading_whitespace_in_tag(self):
        """Some LLMs add space after language tag"""
        response = "```python \nx = 1\n```"
        result = extract(response)
        self.assertIn("x = 1", result)


# -------------
# Fence-less responses  (fallback)

class TestFencelessResponses(unittest.TestCase):
    """LLM returns raw code with no markdown fencing"""

    def test_plain_code_returned_as_is(self):
        """no fences detected - return entire response stripped of leading/trailing whitespace"""
        code = "def bar():\n    return 0"
        self.assertEqual(code, extract(code))

    def test_plain_code_is_stripped(self):
        """Leading/trailing whitespace should be removed even in fence-less responses"""
        code = "\n\ndef bar():\n    return 0\n\n"
        result = extract(code)
        self.assertEqual(result[0], "d")    # no leading newlines
        self.assertEqual(result[-1], "0")   # no trailing newlines


# -------------
# Edge cases & boundary conditions
class TestEdgeCases(unittest.TestCase):
    """Unusual but plausible LLM outputs"""

    def test_incomplete_opening_fence_uses_fallback(self):
        """Never closed fence should fall through to raw-code path."""
        response = "```python\nx = 1"
        # No closing fence - should return whole thing stripped
        result = extract(response)
        self.assertIn("x = 1", result)

    def test_closing_fence_only_uses_fallback(self):
        """Closing fence with no opening fence should not be treated as valid fenced block"""
        response = "x = 1\n```"
        result = extract(response)
        self.assertIn("x = 1", result)

    def test_empty_fenced_block_returns_empty_string(self):
        """Fenced block with no content should return empty string"""
        response = "```python\n\n```"
        result = extract(response)
        self.assertEqual("", result)

    def test_fenced_block_with_only_whitespace_returns_empty_string(self):
        """Fenced block with only spaces/newlines should return empty string"""
        response = "```python\n   \n```"
        result = extract(response)
        self.assertEqual("", result)

    def test_nested_backtick_content_inside_fence(self):
        """Backticks inside code block"""
        code = "s = f'value: `{x}`'"
        response = f"```python\n{code}\n```"
        self.assertIn("`{x}`", extract(response))


if __name__ == "__main__":
    unittest.main()