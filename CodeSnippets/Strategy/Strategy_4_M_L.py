# A simple implementation of the Strategy design pattern in Python

class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def execute(self, input_data):
        return self.strategy.do(input_data)

class StrategyA:
    def do(self, input_data):
        return "Result A"

class StrategyB:
    def do(self, input_data):
        return "Result B"

if __name__ == "__main__":
    context = Context(StrategyA())
    print(context.execute("Input data")) # Output: Result A

    context = Context(StrategyB())
    print(context.execute("Input data")) # Output: Result B