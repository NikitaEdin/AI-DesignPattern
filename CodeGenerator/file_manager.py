"""
File Manager Module

Handles file operations inlcuding directory creation, file naming, ID management, and saving code snippets
"""

import os, re, json
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class FileManager:
    """Manages file operations for code snippets"""

    def __init__(self, base_output_dir: str = ".../CodeSnippets"):
        self.base_output_dir = base_output_dir
        self.ensure_base_directory()

    def ensure_base_directory(self):
        """Ensure base output directory exists"""
        os.makedirs(self.base_output_dir, exist_ok=True)
    
    def get_pattern_directory(self, design_pattern: str) -> str:
        """Get directory path for specific pattern"""
        pattern_dir = os.path.join(self.base_output_dir, design_pattern)
        os.makedirs(pattern_dir, exist_ok=True)
        return pattern_dir
    
    def get_next_id(self, design_pattern: str, difficulty: str, llm_prefix: str) -> int:
        """
        Get the next available ID for code snippet

        Args: 
            design_pattern (str): design pattern
            difficulty (str): difficulty level (E/M/H)
            llm_prefix (str): LLM prefix (L,O,C,K)

        Returns: 
            int: next available ID
        """

        pattern_dir = self.get_pattern_directory(design_pattern)

        # Get all files matching pattern
        pattern_files = []
        for filename in os.listdir(pattern_dir):
            if filename.endswith(".py"):
                # Parse filename: <design_pattern>_<ID>_<difficulty>_<llm_prefix>.py
                match = re.match(rf'^{re.escape(design_pattern)}_(\d+)_{difficulty}_{llm_prefix}\.py$', filename)
                if match:
                    file_id = int(match.group(1))
                    pattern_files.append(file_id)

        # Return next ID (start from 0 if no files exist)
        if not pattern_files:
            return 0
        return max(pattern_files) + 1
                                 
    def generate_filename(self, design_pattern: str, file_id: int, difficulty: str, llm_prefix: str) -> str:
        """
        Generate filename for code snippet

        Format: <design_pattern>_<ID>_<difficulty>_<llm_prefix>.py
        """
        return f"{design_pattern}_{file_id}_{difficulty}_{llm_prefix}.py"

    def save_code_snippet(self, code:str, design_pattern:str, difficulty:str, llm_prefix:str, metadata: Optional[Dict] = None) -> str:
        """
        Save code snippet to file

        Args:
            code (str): code snippet
            design_pattern (str): design pattern
            difficulty (str): difficulty level (E/M/H)
            llm_prefix (str): LLM prefix (L,O,C,K)
            metadata (Optional[Dict]): optional additional metadata to save
        """

        # Get next ID and generate filename
        file_id = self.get_next_id(design_pattern, difficulty, llm_prefix)
        filename = self.generate_filename(design_pattern, file_id, difficulty, llm_prefix)

        # Get pattern directory
        pattern_dir = self.get_pattern_directory(design_pattern)
        file_path = os.path.join(pattern_dir, filename)

        # Prepare content with metadata header
        content = self._prepare_file_content(code, design_pattern, difficulty, llm_prefix, file_id, metadata)

        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return file_path

    def _prepare_file_content(self, code: str, design_pattern: str, difficulty: str, llm_prefix: str, file_id: int, metadata: Optional[Dict]) -> str:
        """Prepare the complete file content with metadata header"""

        # Map LLM prefix to full name
        llm_name = {
            'L': 'Ollama (codeLlama)',
            'O': 'OpenAI',
            'C': 'Claude',
            'K': 'Kimi K2'
        }

        # Map difficulty codes to description
        difficulty_desc = {
            'E': 'Easy',
            'M': 'Medium',
            'H': 'Hard'
        }

        llm_name = llm_name.get(llm_prefix, 'Unknown')
        difficulty_name = difficulty_desc.get(difficulty, 'Unknown')

        # Create metadata header
        header = f'''"""
Code Snippet: {design_pattern} Pattern Implementation

Created by: {llm_name}
Pattern: {design_pattern}
Difficulty: {difficulty_name} ({difficulty})
ID: {file_id}
Generated on: {datetime.now().strftime("d-%m-%Y %H:%M:%S")}
"""

'''
      # Add medata if provided
        if metadata:
            header += f'# Metadata: {json.dumps(metadata, indent=2)}\n\n'
        return header + code

    def get_existing_files_info(self, design_pattern:str) -> List[Dict]:
        """
        Get Information about existing files for a design pattern 
        Returns list of dictionaries with file information
        """

        pattern_dir = self.get_pattern_directory(design_pattern)
        files_info = []

        for filename in os.listdir(pattern_dir):
            if filename.endswith('.py'):
                # Parse filename
                match = re.match(rf'^{re.escape(design_pattern)}_d(\d+)_([MEH]_([LOCK])\.py)', filename)
                if match:
                    file_id = int(match.group(1))
                    difficulty = match.group(2)
                    llm_prefix = match.group(3)
                    file_path = os.path.join(pattern_dir, filename)

                    files_info.append({
                        'filename': filename,
                        'path': file_path,
                        'id': file_id,
                        'difficulty': difficulty,
                        'llm_prefix': llm_prefix,
                        'size': os.path.getsize(file_path)
                    })

        return sorted(files_info, key=lambda x: (x['difficulty'], x['llm_prefix'], x['id']))
    
    def cleanup_failed_files(self, pattern_dir:str, max_size: int = 100):
        """
        Removes files that are too small (likely failed generation or corrupted)"""
        for filename in os.listdir(pattern_dir):
            if filename.endswith('.py'):
                file_path = os.path.join(pattern_dir, filename)
                if os.path.getsize(file_path) < max_size:
                    try:
                        os.remove(file_path)
                        print(f"Removed small/failed file: {filename}")
                    except Exception as e:
                        print(f"Could not remove {filename}: {e}")