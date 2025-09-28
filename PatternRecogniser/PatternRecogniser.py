# Used to include SHARED dir - don't remove
from report_generator import ReportGenerator
import add_shared as _

import argparse, sys
from catalogue import WorkflowType
from shared.llm_interface import LLMFactory
from single_workflow import SingleWorkflow
from cli import create_argument_parser, validate_arguments
from file_manager import FileManager

class DPR:

    def __init__(self):
        self.filemanager = FileManager()

    def run(self, args: argparse.Namespace):
        # workflow to use
        self.workflow = args.workflow
        # llm to use for analysis
        self.llm = args.llm

        # filters
        self.count = args.count
        self.filter_pattern = args.filter_pattern
        self.filter_difficulty = args.filter_difficulty
        self.filter_llm = args.filter_llm

        # print(f'---analysing---')
        # print(f'self.workflow: {self.workflow}')
        # print(f'self.llm: {self.llm}')
        # print(f'---filters---')
        # print(f'self.pattern: {self.filter_pattern}')
        # print(f'self.difficulty: {self.filter_difficulty}')
        # print(f'self.filter_llm: {self.filter_llm}')
        # print(f'self.count: {self.count}')
        
        # Get code snippets
        files = self.filemanager.locate_snippets(
            design_pattern=self.filter_pattern, 
            difficulty=self.filter_difficulty,
            llm=self.filter_llm,
            count=self.count)
        
        # for file in files:
        #     print(file)

        print(f"Found {len(files)} code snippets to analyse")
        
        if not files:
            print("No code snippets found matching the criteria.")
            return
        
        # init LLM
        llm_interface = LLMFactory.create_llm(self.llm)

        # Select and run workflow
        if self.workflow == WorkflowType.SINGLE_PROMPT:
            workflow = SingleWorkflow(llm_interface)
        elif self.workflow == WorkflowType.MULTI_LAYERED:
            print("[DEV] Multilayered workflow is not yet implemented.")
            sys.exit(1)
        else:
            raise ValueError(f"Unknown workflow: {self.workflow}")
        
        # Execute the workflow
        results = workflow.execute(files)
        
        # Report
        if results:
            report_gen = ReportGenerator()
            report_gen.save_results(results, llm_interface)


def main(argv=None):
   # CLI args
   raw_args = create_argument_parser().parse_args()
   # Validate and normalise
   args = validate_arguments(raw_args)
   # Execute DesignPatternRecogniser with validated args
   app = DPR()
   app.run(args)

if __name__ == "__main__":
    main()
