# Strategy pattern implementation

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self):
        return self.strategy.algorithm()

class Strategy:
    def algorithm(self):
        raise NotImplementedError("This is a pure abstract class.")

class ConcreteStrategyA(Strategy):
    def algorithm(self):
        return "Algorithm A"

class ConcreteStrategyB(Strategy):
    def algorithm(self):
        return "Algorithm B"

if __name__ == "__main__":
    context = Context(ConcreteStrategyA())
    print(context.execute_strategy())  # Output: Algorithm A
    context = Context(ConcreteStrategyB())
    print(context.execute_strategy())  # Output: Algorithm B