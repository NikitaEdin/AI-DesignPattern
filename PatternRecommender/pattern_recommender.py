import sys
from typing import Dict, Any

# Add parent directories for SHARED

from shared.llm_interface import LLMFactory
from cli import CLI
from interactive_workflow import InteractiveWorkflow

def display_results(recommendation: Dict[str, Any]) -> None:
    """Display final results"""
    print("\nFINAL RECOMMENDATION\n" + "="*60 + "\n")
    
    
    print(f"Current Pattern: {recommendation.get('current_pattern', 'None')}")
    print(f"Recommended: {recommendation.get('recommendation_type', 'Unknown')}")
    print(f"Suggested Pattern: {recommendation.get('suggested_pattern', 'None')}")
    print(f"Confidence: {recommendation.get('confidence', 0.0):.2f}")
    
    if recommendation.get('rationale'):
        print(f"\nRationale:\n{recommendation['rationale']}")
    
    if recommendation.get('benefits'):
        print(f"\nBenefits:\n{recommendation['benefits']}")

def main():
    try:
        # Parse args
        cli = CLI()
        args = cli.parse_args()

        # Validate file
        file_path = cli.validate_file(args.file)
        if not file_path:
            return 1
        
        # Read code
        code_content = cli.read_code_file(file_path)
        if not code_content:
            return 1
        
        # Generate output paths
        result_path = cli.get_output_path(args.file, suffix='_result')
        #log_path = cli.get_output_path(args.file, suffix='_log')

        ## LLM interface
        try:
            llm_interface = LLMFactory.create_llm(args.llm)
        except ValueError as e:
            print(f"[Error] {str(e)}", file=sys.stderr)
            print(f"Available LLMs: {', '.join(LLMFactory.get_available_providers())}")
            return 1
        
        # Display header
        print("\nDesign Pattern Recommender Agent\n" + "=" * 60)
        print(f"Input: {args.file}\nOutput: {result_path.name}")
        print(f"LLM: {args.llm} ({llm_interface.get_prefix()})")

        # Workflow
        workflow = InteractiveWorkflow(llm_interface)
        recommendation = workflow.execute(code_content, file_path.name)

        # Display results
        display_results(recommendation)

        # Save code (if any)       
        code_generated = recommendation.get('code_generated', False)
        
        if code_generated and recommendation.get('recommended_code'):
            cli.save_output(result_path, recommendation['recommended_code'])
            print(f'[Success] Generated code saved to: {result_path.name}')
    
        if not code_generated:
            # If no code generated, inform user
            print("\n" + "="*60 + "\nNOTE: Code generation was declined by user" + "\n" + "="*60)
        
        return 0

    except Exception as e:
        print(f"[Error] {str(e)}", file=sys.stderr)
        return 1 
    

if __name__ == '__main__':
    sys.exit(main())