from dataclasses import dataclass
import os
import re
from typing import Any, Dict, List, Optional
from catalogue import get_llm_prefix

@dataclass
class CodeSnippet:
    """Code snippet with metadata"""
    filepath: str
    filename: str
    content: str
    design_pattern: Optional[str] = None
    difficulty: Optional[str] = None
    llm: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class FileManager:
    def __init__(self, base_out_dir: str = "../CodeSnippets"):
        self.base_output_dir = base_out_dir
        self.ensure_base_directory()

    def ensure_base_directory(self):
        """Ensure base output directory exists"""
        os.makedirs(self.base_output_dir, exist_ok=True)

    def get_pattern_directory(self, design_pattern: str) -> str:
        """Get directory path for specific pattern"""
        pattern_dir = os.path.join(self.base_output_dir, design_pattern)
        os.makedirs(pattern_dir, exist_ok=True)
        return pattern_dir

    def locate_snippets( self,
        design_pattern: Optional[str] = None,
        difficulty: Optional[str] = None,
        llm: Optional[str] = None,
        count: int = -1,
    ) -> List[str]:
        """
        Return absolute paths to *.py code snippets that match given filters.
        Code snippets must follow the pattern: "<pattern>_<id>_<difficulty>_<llm>.py"
        Unspecified filters will be ignored.
        Count=-1 will return all matches
        """

        code_snippets: List[str] = []

        # Pattern
        if design_pattern:
            patterns_to_scan = [design_pattern]
        else:
            # Set all folders as patterns to scan (scan all)
            patterns_to_scan = [ d for d in os.listdir(self.base_output_dir)
                                if os.path.isdir(os.path.join(self.base_output_dir, d))]
        
        
        llm_prefix = get_llm_prefix(llm) if llm else None

        # Use REGEX to filter
        pattern_re = re.escape(design_pattern) if design_pattern else r"[^_]+" 
        diff_re = re.escape(difficulty) if difficulty else r"[EMH]"
        llm_re = re.escape(llm_prefix) if llm_prefix else r"[^_]+"

        # Compile reg
        file_regex = re.compile(rf"^{pattern_re}_\d+_{diff_re}_{llm_re}\.py$", re.IGNORECASE)

        # Scan pattern in each code snippet folder
        for pattern in patterns_to_scan:
            pattern_folder = self.get_pattern_directory(pattern)
            for filename in os.listdir(pattern_folder):
                if not filename.endswith(".py"):
                    continue # skip non python files

                if file_regex.match(filename):
                    filepath = os.path.join(pattern_folder, filename)

                    # Split filename parts and autoassign to variables
                    name_parts = filename[:-3].split("_") 
                    metadata_pattern, _, metadata_difficulty, metadata_llm = name_parts

                    content = ""
                    # Read content
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    code_snippets.append(CodeSnippet(
                        filepath=filepath,
                        filename=filename,
                        content=content,
                        difficulty=metadata_difficulty,
                        design_pattern=metadata_pattern,
                        llm=metadata_llm
                    ))
            
        # Limit by count (if any)
        if count > 0:
            code_snippets = code_snippets[:count]

        return code_snippets
    
    def locate_snippet(self, filename: str) -> List[CodeSnippet]:
        code_snippets: List[str] = []

        filename = filename.lower()
        if not filename.endswith(".py"):
            filename += ".py"

        # every pattern folder
        for pattern in os.listdir(self.base_output_dir):
            pattern_dir = os.path.join(self.base_output_dir, pattern)
            if not os.path.isdir(pattern_dir):
                continue

            for fname in os.listdir(pattern_dir):
                if fname.lower() == filename and fname.endswith(".py"):
                    filepath = os.path.join(pattern_dir, fname)

                    # Parse filename
                    name_parts = fname[:-3].split("_")
                    if len(name_parts) != 4:
                        continue
                    pattern, _id, difficulty, llm = name_parts
                    
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    code_snippets.append(CodeSnippet(
                        filepath=filepath,
                        filename=fname,
                        content=content,
                        difficulty=difficulty,
                        design_pattern=pattern,
                        llm=llm
                    ))
        print(len(code_snippets))
        return code_snippets

    def locate_custom_snippet(self, filepath: str) -> List[CodeSnippet]:
        """Load custom code snippet"""
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = os.path.basename(filepath)
        
        snippet = CodeSnippet(
            filepath=filepath,
            filename=filename,
            content=content,  
            design_pattern='Unknown',  # pattern unknown
            difficulty='Unknown',      
            llm='Unknown')                  
        
        return [snippet]

