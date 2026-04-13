# Used to include SHARED dir - don't remove
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import argparse
import sys
from report_generator import ReportGenerator
from catalogue import WorkflowType
from shared.llm_interface import LLMFactory
from single_workflow import SingleWorkflow
from cli import create_argument_parser, validate_arguments
from file_manager import FileManager

class DPR:
    def __init__(self,  file_manager: FileManager = None, llm_factory = None, 
                 workflow_factory=None, report_generator_factory=None):
        self.file_manager = file_manager or FileManager()
        self.llm_factory = llm_factory or LLMFactory.create_llm
        self.workflow_factory = workflow_factory or DPR._default_workflow_factory
        self.report_generator_factory = report_generator_factory or ReportGenerator
        
    ############### Utils ###############
    @staticmethod
    def _default_workflow_factory(workflow_type: WorkflowType, llm_interface):
        if workflow_type == WorkflowType.SINGLE_PROMPT:
            return SingleWorkflow(llm_interface)
        if workflow_type == WorkflowType.MULTI_LAYERED:
            raise NotImplementedError(
                "[DEV] Multilayered workflow is not yet implemented."
            )
        raise ValueError(f"Unknown workflow: {workflow_type}")

    def _load_files(self, args: argparse.Namespace):
        if args.input_path:
            files = self.file_manager.locate_custom_snippet(args.input_path)
            return files, True
        files = self.file_manager.locate_snippets(
            design_pattern=args.filter_pattern,
            difficulty=args.filter_difficulty,
            llm=args.filter_llm,
            count=args.count,
        )
        return files, False
    
    def _save_results(self, results, llm_interface, custom_input_mode: bool):
        report_gen = self.report_generator_factory()
        if custom_input_mode:
            report_gen.save_custom_results(results)
        else:
            report_gen.save_results(results, llm_interface)

    def _print_results(self, results):
        print(f"\n{'─' * 30}")
        print("Results")
        print(f"\n{'─' * 30}")
        for r in results:
            filename = os.path.basename(r.snippet_path)
            match = "[Success]" if r.expected_pattern == r.identified_pattern else "[Failure]"
            print(f"File:             {filename}")
            print(f"Expected:         {r.expected_pattern}")
            print(f"Identified:       {r.identified_pattern} {match}")
            print(f"Confidence:       {r.confidence:.0%}")
            print(f"Difficulty:       {r.difficulty}")
            print(f"Analysis time:    {r.analysis_time:.2f}s")
            print(f"{'─' * 30}")

    ########### Main workflow ############
    def run(self, args: argparse.Namespace):
        # Resolve files and detect input mode
        files, custom_input_mode = self._load_files(args)
        print(f"Found {len(files)} code snippets to analyse")
 
        if not files:
            print("No code snippets found matching the criteria.")
            return
 
        # Init LLM
        llm_interface = self.llm_factory(args.llm)
 
        # Create workflow
        try:
            workflow = self.workflow_factory(args.workflow, llm_interface)
        except NotImplementedError as exc:
            print(exc)
            sys.exit(1)

        ## Execute workflow
        results = workflow.execute(files)

        # Save results (if any)
        if results:
            if args.dont_save:
                self._print_results(results)
            else:
                self._save_results(results, llm_interface, custom_input_mode)


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
