import argparse
import sys
from enum import Enum

# TODO: move to its own/util python script
class WorkflowType(Enum):
    SINGLE_PROMPT = "single_prompt"
    MULTI_LAYERED = "multi_layered" 

##################### ARGUMENT PARSER & MAIN  #####################

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Design Pattern Recogniser - Analyse code snippets to identify design patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
 python PatternRecogniser.py analyse --all
 python PatternRecogniser.py analyse --pattern Adapter
 python PatternRecogniser.py analyse --difficulty E
 python PatternRecogniser.py analyse --llm c
 python PatternRecogniser.py analyse --pattern singleton --llm c
 python PatternRecogniser.py analyse --pattern singleton --llm c --difficulty E


Available Design Patterns:
 Singleton, Factory, Builder, Prototype,
 Adapter, Decorator, Facade, Proxy,
 Observer, Strategy, Command, Iterator, State

Difficulty Levels:
 E = Easy (basic implementation)
 M = Medium (standard implementation with features)
 H = Hard (complex implementation with advanced features)

LLM Providers:
 ollama - Local Ollama
 openai - OpenAI GPT  
 claude - Anthorpic Claude
 grok - xAI Grok 4 Fast
 kimi - Kimi K2
"""
    )

    parser.add_argument('--all', '-a', 
        action='store_true', 
        help='Analyse ALL snippets.'
    )

    parser.add_argument('--pattern', '-p', 
        type=str, 
        help='Filter by pattern name', 
        default='Singleton')
    
    parser.add_argument('--difficulty', '-diff', 
        type=str, choices=['E', 'M', 'H'], 
        default='E', 
        help='Filter by difficulty (E=Easy, M=Medium, H=Hard)'
    )

    parser.add_argument('--llm', 
        type=str, 
        help='Filter by LLM identify (C=Claude, O=OpenAI, etc.)',
        default='openai'
    )
    parser.add_argument('--workflow', '-w', 
        type=str, 
        choices=['single', 'multi'], 
        default='single', 
        required=True,
        help='Analyse workflow type'
    )

    parser.add_argument('--count', '-c',
                        type=int,
                        default=-1,
                        help='Total code snippets to process/analyse.')

    return parser


class DPR:

    def __init__(self):
        # Common design patterns
        self.design_patterns = [
            "Singleton", "Factory", "Builder", "Prototype",
            "Adapter", "Decorator", "Facade", "Proxy",
            "Observer", "Strategy", "Command", "Iterator", "State"
        ]

        self.difficulty_levels = ['E', 'M', 'H']  # Easy, Medium, Hard
        self.llm_providers = ['openai', 'claude', 'kimi', 'grok', 'ollama']


    def run(self, args: argparse.Namespace):
        try:

            # Validate starting args
            self._validate_arguments(args)


            selected_llm = args.llm
            selected_difficulty = args.difficulty
            selected_pattern = args.pattern
            workflow_type = self.workflow_type
            count = args.count

            print(f"type: {workflow_type}")
            print(f"selected_llm: {selected_llm}")
            print(f"selected_difficulty: {selected_difficulty}")
            print(f"selected_pattern: {selected_pattern}")
            print(f"count: {count}")


        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)




    def _validate_arguments(self, args: argparse.Namespace):
        """Validate command line arguments"""

        # Workflow type
        self.workflow_type = WorkflowType.SINGLE_PROMPT
        if args.workflow == 'multi':
            self.workflow_type = WorkflowType.MULTI_LAYERED

        # Design Pattern
        if args.pattern not in self.design_patterns:
            print(f"Error: Unknown design pattern '{args.pattern}'")
            print(f"Available patterns: {', '.join(self.design_patterns)}")
            sys.exit(1)

        # Complexity level
        if args.difficulty not in self.difficulty_levels:
            print(f"Error: Invalid difficulty level '{args.difficulty}'")
            print(f"Available levels: {','.join(self.difficulty_levels)} (E=Easy, M=Medium, H=Hard)")
            sys.exit(1)

        # LLM provider    
        if args.llm not in self.llm_providers:
            print(f"Error: Unsupposrted LLM provider '{args.llm}'")
            print(f"Available providers: {', '.join(self.llm_providers)}")
            sys.exit(1)
        
        
    
        

def analyse_command(args):
    # Workflow type
    workflow_type = WorkflowType.SINGLE_PROMPT
    if args.workflow == 'multi':
        workflow_type = WorkflowType.MULTI_LAYERED

    # Check filters or --all is used
    if not (args.all or args.pattern or args.difficulty or args.llm):
        print(f"Error: must specify --all or at least one filter (--pattern, --difficulty, --llm)")
    

def main(argv=None):
    # Parse args
    parser = create_argument_parser()
    args = parser.parse_args(argv)

    app = DPR()
    app.run(args)

if __name__ == "__main__":
    main()
