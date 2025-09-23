class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def execute(self, input_data):
        return self.strategy.execute(input_data)
    
class StrategyA:
    def execute(self, input_data):
        print("Strategy A executed with input data:", input_data)
        return "result from strategy a"
    
class StrategyB:
    def execute(self, input_data):
        print("Strategy B executed with input data:", input_data)
        return "result from strategy b"
    
if __name__ == "__main__":
    context = Context(StrategyA())
    result = context.execute("input data")
    print("Result:", result)