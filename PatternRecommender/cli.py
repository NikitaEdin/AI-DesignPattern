"""
CLI Interface for DPR Agent - Handles command-line args
"""

import argparse, sys
from pathlib import Path
from typing import Optional

# Add parent folder for shared folder
sys.path.append(str(Path(__file__).parent.parent))

# Factory for LLM providers
from shared.llm_interface import LLMFactory

class CLI:
    """CLI interface for pattern recommendation"""

    # Max lines to read from file - avoid overload on LLMs
    MAX_LINES = 200
    BASE_DIR = Path(__file__).parent

    # Directories for input and output
    INPUT_DIR = BASE_DIR / "Input"
    OUTPUT_DIR = BASE_DIR / "Output"

    def __init__(self):
        self.parser = self._create_parser()
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure Input and Output directories exist"""
        self.INPUT_DIR.mkdir(exist_ok=True)
        self.OUTPUT_DIR.mkdir(exist_ok=True)

    # Parser

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and init argument parser """
        parser = argparse.ArgumentParser(
            description="AI-powered Design Pattern Recommender Agent",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
Examples:
  python pattern_recommender.py my_code.py openai
  python pattern_recommender.py code_snippet1.py kimi
  python pattern_recommender.py code.py claude

Notes:
  Files are read from "/PatternRecommender/Input" directory.
  Results are saved into "/PatternRecommender/Output" directory.

Available LLMs: {', '.join(LLMFactory.get_available_providers())}
            """
        )

        # File
        parser.add_argument(
            'file',
            type=str,
            help="Python file (.py) to analyse from /PatternRecommender/Input directory"
        )

        # LLM - the LLM provider that will be used
        parser.add_argument(
            'llm',
            type=str,
            choices=LLMFactory.get_available_providers(),
            help='LLM to use for analysis'
        )

        return parser
    
    def parse_args(self, args: Optional[list] = None):
        """Parse args"""
        return self.parser.parse_args(args)
    
    # Reading and validating

    def validate_file(self, filename:str) -> Optional[Path]:
        """Validate that the given file exists"""
        file_path = self.INPUT_DIR / filename

        if not file_path.exists():
            print(f'[Error] File not found in ./Input: {filename}', file=sys.stderr)
            print(f'[Error] Looking for: {file_path.absolute()}', file=sys.stderr)
            return None
        
        if file_path.suffix != '.py':
            print(f'[Error] Only Python files (.py) are supported.', file=sys.stderr)
            return None
        
        return file_path

    def read_code_file(self, file_path: Path) -> Optional[str]:
        """Read and validate provided file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if len(lines) > self.MAX_LINES:
                print(f'[Error] File exceeds max {self.MAX_LINES} lines (found {len(lines)})', file=sys.stderr)
                return None
            
            return ''.join(lines)
        
        except Exception as e:
            print(f'[Error] Failed to reach file: {str(e)}', file=sys.stderr)
            return None

    # Saving
    def save_output(self, output_path: Path, code: str) -> bool:
        """Save to file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f'[Info] Recommended code saved to: ./Output/{output_path.name}')
            return True
        except Exception as e:
            print(f'[Error] Could not save output file: {str(e)}', file=sys.stderr)
            return False
        
    def save_log(self, log_path: Path, log_content: str ) -> bool:
        """Save log"""
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            print(f'[Info] Log saved to: ./Output/{log_path.name}')
            return True
        except Exception as e:
            print(f'[Error] Failed to save log file: {str(e)}', file=sys.stderr)
            return False




