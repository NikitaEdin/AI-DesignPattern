class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def execute(self):
        return self.strategy.do_something()

class StrategyA:
    def do_something(self):
        return "Strategy A executed"

class StrategyB:
    def do_something(self):
        return "Strategy B executed"

def main():
    context = Context(StrategyA())
    print(context.execute())  # Output: Strategy A executed
    
    context = Context(StrategyB())
    print(context.execute())  # Output: Strategy B executed

if __name__ == "__main__":
    main()