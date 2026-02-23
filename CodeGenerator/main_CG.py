import argparse, sys, time, os

from llm_interface import LLMInterface, LLMFactory
from code_generator import CodeSnippetGenerator
from file_manager import FileManager

class CodeGenerator:
    """ Main class for code generation using design patterns """

    def __init__(self):
        # File Manager
        self.file_manager = FileManager()

        # Common design patterns
        self.design_patterns = [
            "Singleton", "Factory", "Builder", "Prototype",
            "Adapter", "Decorator", "Facade", "Proxy",
            "Observer", "Strategy", "Command", "Iterator", "State"
        ]

        self.difficulty_levels = ['E', 'M', 'H']  # Easy, Medium, Hard
        self.llm_providers = list(LLMFactory.get_available_providers())

    def run(self, args: argparse.Namespace):
        try:

            # Validate starting args
            self._validate_arguments(args)

            selected_llm = args.llm
            selected_count = args.count
            selected_difficulty = args.difficulty
            selected_pattern = args.pattern

            # Create LLM interface
            llm = self._create_llm_interface(selected_llm)
            # Create code generator 
            generator = CodeSnippetGenerator(llm)

            # Generate code snippets
            success_count, failed_count = self._generate_snippets(
                generator, selected_pattern, selected_count, selected_difficulty, llm.get_prefix()
            )

            # Results
            self._display_results(success_count, failed_count, selected_pattern)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

    def _create_llm_interface(self, provider: str) -> LLMInterface:
        """ Create LLM interface based on provider """
        try:
            llm = LLMFactory.create_llm(provider)

            # Test the connection with simple prompt
            print(f"Testing connection to {provider} LLM...")
            test_response = llm.generate_response("Hello, respond with 'Connection successful!'")

            if "successful" in test_response.lower() or len(test_response) > 0:
                print(f"Connection to {provider} LLM successful.")
                return llm
            else:
                raise Exception(f"Connection test failed for {provider} LLM.")
            
        except Exception as e:
            print(f"Failed to connect to {provider} LLM: {str(e)}")
            if provider == "ollama":
                print("Ensure Ollama is running locally and the model is available.")
            elif provider in ["openai", "claude", "kimi"]:
                print(f"Check your API key and network connection for {provider}.")
            sys.exit(1)

    def _display_generation_info(self, args: argparse.Namespace):
        pass

    def _generate_snippets(self, generator: CodeSnippetGenerator, pattern: str, count: int, difficulty: str, llm_prefix: str) -> tuple:
        """ Generate the specified number of code snippets"""

        success_count = 0
        failed_count = 0
        for i in range(count):
            print(f"\nGenerating snippets {i+1}/{count}...")
            try:
                # Generate code snippet
                start_time = time.time()
                code, is_valid, feedback = generator.generate_code_snippet(pattern, difficulty)
                generation_time = time.time() - start_time

                if is_valid and code:

                    metadata = {
                        "generation_time": round(generation_time, 2),
                        "evaluation_feedback": feedback,
                        "is_valid": is_valid
                    }

                    # Save to file
                    file_path = self.file_manager.save_code_snippet(
                        code, pattern, difficulty, llm_prefix, metadata
                    )

                    print(f"[SUCCESS] Generated and saved: {os.path.basename(file_path)}")
                    print(f"[INFO] Time: {generation_time:.2f} seconds")

                    success_count += 1
                else:
                    print(f" Generation failed: {feedback}")
                    failed_count += 1
            except Exception as e:
                print(f" Error generating snippet {i+1}: {str(e)}")
                failed_count += 1

        return success_count, failed_count


    def _display_results(self, success_count: int, failed_count: int, pattern: str):
        """Display generation results summary"""

        total = success_count + failed_count

        print("\n" + "="*60)
        print("GENERATION RESULTS")
        print("="*60)
        print(f"Total attempted: {total}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failed_count}")

        if success_count > 0:
            success_rate = (success_count / total) * 100
            print(f"Success rate: {success_rate:.1f}%")

            files_info = self.file_manager.get_existing_files_info(pattern)
            if files_info:
                print(f"\nExisting files for {pattern}:")
                
                for file_info in files_info[-5:]: # last 5 fiels
                    print(f"  {file_info['filename']} ({file_info['size']} bytes)")
                if len(files_info) > 5:
                    print(f"  ... and {len(files_info) - 5} more files")
        print("="*60)

    def _validate_arguments(self, args: argparse.Namespace):
        """Validate command line arguments"""

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

        if args.count <= 0:
            print(f"Error: Count must be a positive integer")
            sys.exit(1)
        



##################### ARGUMENT PARSER & MAIN  #####################

def create_argument_parser() -> argparse.ArgumentParser:
    """ Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description="Generate code snippet using design patterns and various LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
python main_CG.py --pattern Singleton --count 5 --llm grok --difficulty M
python main_CG.py --pattern Factory --count 3 --llm openAI --difficulty H

Available Design Patterns:
Singleton, Factory, Builder, Prototype,
Adapter, Decorator, Facade, Proxy,
Observer, Strategy, Command, Iterator, State

Difficulty Levels:
E = Easy (basic implementation)
M = Medium (standard implementation with features)
H = Hard (complex implementation with advanced features)

LLM Providers:
grok - Grok-code-fast-1
openai - OpenAI GPT  
claude - Anthorpic Claude
kimi - Kimi K2
"""
    )

    parser.add_argument(
        "--pattern", "-p",
        required=True,
        help="Design pattern to implement"
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of code snippets to generate (default: 1)"
    )
    
    # parser.add_argument(
    #     "--llm", "-l",
    #     default="ollama",
    #     help="LLM provider to use (default: ollama)"
    # )
    
    parser.add_argument(
        "--difficulty", "-d",
        default="M",
        help="Difficulty level: E(asy), M(edium), H(ard) (default: M)"
    )

    return parser
    

def main(argv=None):
    # Parse args
    parser = create_argument_parser()
    args = parser.parse_args(argv)

    app = CodeGenerator()
    app.run(args)

if __name__ == "__main__":
    main()

        