import argparse
from cli import create_argument_parser, validate_arguments

class DPR:

    def __init__(self):
        pass

    def run(self, args: argparse.Namespace):
        self.workflow = args.workflow
        self.llm = args.llm
        self.pattern = args.pattern
        self.difficulty = args.difficulty
        self.count = args.count
        self.all_flag = args.count < 0

        print(f"self.workflow: {self.workflow}")
        print(f"self.llm: {self.llm}")
        print(f"self.pattern: {self.pattern}")
        print(f"self.difficulty: {self.difficulty}")
        print(f"self.count: {self.count}")
        print(f"self.all_flag: {self.all_flag}")
        pass
           

    

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
