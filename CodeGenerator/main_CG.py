import argparse, sys, time

from llm_interface import LLMInterface, LLMFactory
from code_generator import CodeSnippetGenerator

class CodeGenerator:
    """ Main class for code generation using design patterns """

    def __init__(self):
        # Common design patterns
        self.design_patterns = [
            "Singleton", "Factory", "Observer",
            "Decorator", "Strategy", "Adapter",
            "Command", "Facade", "Builder"
            "Prototype", "Proxy", "State"
        ]

        self.difficulty_levels = ['E', 'M', 'H']  # Easy, Medium, Hard
        self.llm_providers = ["ollama"]
        # TODO: Add more providers when implemented - openai, claude, kimi k2

    def run(self, args: argparse.Namespace):
        try:
            # Create LLM interface
            llm = self._create_llm_interface("ollama")
            # Create code generator 
            generator = CodeSnippetGenerator(llm)

            # Generate code snippets
            success_count, failed_count = self._generate_snippets(
                generator, "Singleton", 1, 'E', llm.get_prefix()
            )

            # Results
            self._display_results(success_count, failed_count, "Singleton")
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

                    # print(f"[DEBUG] Generated Code Snippet:\n{code}")
                    # print(f"[DEBUG] Metadata: \N{metadata}")

                    # TODO: Save to file

                    success_count += 1
                else:
                    print(f" Generation failed: {feedback}")
                    failed_count += 1
            except Exception as e:
                print(f" Error generating snippet {i+1}: {str(e)}")
                failed_count += 1

        return success_count, failed_count


    def _display_results(self, success_count: int, failed_count: int, pattern: str):
        pass



def main():
    #TODO: add argparse for more options

    app = CodeGenerator()
    app.run(args = None)

if __name__ == "__main__":
    main()

        