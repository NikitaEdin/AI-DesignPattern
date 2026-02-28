import re
import sys
import os

# Repo root & CodeGenerator directory added to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../CodeGenerator')))

import unittest
from CodeGenerator.file_manager import FileManager



# --------------
# Shared
def make_manager(tmp_dir):
    """Return a FileManager rooted at a temporary directory."""
    return FileManager(base_output_dir=tmp_dir)


def touch(path, content=""):
    """Write content to a file, creating it if needed."""
    with open(path, 'w') as f:
        f.write(content)



#---------------
# generate_filename
class TestGenerateFilename(unittest.TestCase):
    """Pure function — format must be <pattern>_<id>_<difficulty>_<prefix>.py"""
    def setUp(self):
        self.mgr = FileManager.__new__(FileManager)


    # Format Tests
    def test_basic_output(self):
        """Basic case with typical inputs"""
        self.assertEqual(self.mgr.generate_filename("Singleton", 0, "E", "C"), "Singleton_0_E_C.py")

    def test_format_has_four_parts_separated_by_underscores(self):
        """Filename contains 4 parts separated by underscores"""
        name = self.mgr.generate_filename("Observer", 1, "M", "L")
        stem = name.removesuffix(".py")
        self.assertEqual(stem.split("_"), ["Observer", "1", "M", "L"])

    def test_ends_with_py_extension(self):
        """Filename ends with .py extension"""
        name = self.mgr.generate_filename("Singleton", 0, "E", "C")
        self.assertTrue(name.endswith(".py"))

    # Parameter presence tests
    def test_each_parameter_present_in_output(self):
        """Each parameter present in filename"""
        name = self.mgr.generate_filename("Factory", 0, "E", "C")
        self.assertIn("Factory", name)
        name = self.mgr.generate_filename("Singleton", 117, "E", "C")
        self.assertIn("117", name)
        name = self.mgr.generate_filename("Singleton", 0, "H", "C")
        self.assertIn("H", name)
        name = self.mgr.generate_filename("Singleton", 0, "E", "K")
        self.assertIn("K", name)


    # Different inputs produce different outputs
    def test_different_pattern_changes(self):
        # pattern
        a = self.mgr.generate_filename("Singleton", 0, "E", "C")
        b = self.mgr.generate_filename("Observer",  0, "E", "C")
        self.assertNotEqual(a, b)
        # file_id
        a = self.mgr.generate_filename("Singleton", 0, "E", "C")
        b = self.mgr.generate_filename("Singleton", 1, "E", "C")
        self.assertNotEqual(a, b)
        # difficulty
        a = self.mgr.generate_filename("Singleton", 0, "E", "C")
        b = self.mgr.generate_filename("Singleton", 0, "H", "C")
        self.assertNotEqual(a, b)
        # prefix
        a = self.mgr.generate_filename("Singleton", 0, "E", "C")
        b = self.mgr.generate_filename("Singleton", 0, "E", "L")
        self.assertNotEqual(a, b)

    # Regex test
    def test_filename_matches_get_next_id_regex(self):
        pattern, difficulty, prefix = "Singleton", "E", "C"
        name = self.mgr.generate_filename(pattern, 3, difficulty, prefix)
        regex = re.compile(rf'^{re.escape(pattern)}_(\d+)_{difficulty}_{prefix}\.py$')
        self.assertIsNotNone(regex.match(name))

if __name__ == "__main__":
    unittest.main()