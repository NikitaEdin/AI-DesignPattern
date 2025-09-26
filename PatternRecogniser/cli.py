import argparse
import sys

from catalogue import WorkflowType, DESIGN_PATTERNS, DIFFICULTY_LEVELS,LLM_PROVIDERS, LLM_SHORT_MAP

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


def validate_arguments(args: argparse.Namespace) -> argparse.Namespace:
        """Validate and normalise command line arguments"""

        # Workflow type
        if args.workflow == 'multi':
            args.workflow = WorkflowType.MULTI_LAYERED
        else:
            args.workflow = WorkflowType.SINGLE_PROMPT

        # Design Pattern
        if args.pattern not in DESIGN_PATTERNS:
            print(f"Error: Unknown design pattern '{args.pattern}'")
            print(f"Available patterns: {', '.join(DESIGN_PATTERNS)}")
            sys.exit(1)

        # Complexity level
        if args.difficulty not in DIFFICULTY_LEVELS:
            print(f"Error: Invalid difficulty level '{args.difficulty}'")
            print(f"Available levels: {','.join(DIFFICULTY_LEVELS)} (E=Easy, M=Medium, H=Hard)")
            sys.exit(1)

        # LLM provider    
        llm = LLM_SHORT_MAP.get(args.llm, args.llm)
        if llm not in LLM_PROVIDERS:
            print(f"Error: Unsupposrted LLM provider '{args.llm}'")
            print(f"Available providers: {', '.join(LLM_PROVIDERS)}")
            sys.exit(1)
        args.llm = llm

        print(f"COUNT: { args.count}")

        if args.count != -1 and args.count < 0:  
            args.count = -1
        elif args.count == 0:
            print("Count cannot be 0, use -1 for ALL or a positive number.")
            sys.exit(1)
        
        return args