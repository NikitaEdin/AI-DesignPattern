import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directories for SHARED
import add_shared as _

from shared.llm_interface import LLMFactory
from cli import CLI

def main():
    try:
        # Parse args
        cli = CLI()
        args = cli.parse_args()

        print(f'Args-file: {args.file}')
        print(f'Args-llm: {args.llm}')

    except Exception as e:
        print(f"[Error] {str(e)}", file=sys.stderr)
        return 1 
    

if __name__ == '__main__':
    sys.exit(main())