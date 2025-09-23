# A base class for all strategies
class Strategy:
    def do_something(self):
        raise NotImplementedError()

# Concrete strategy 1
class ConcreteStrategy1(Strategy):
    def do_something(self):
        print("ConcreteStrategy1")

# Concrete strategy 2
class ConcreteStrategy2(Strategy):
    def do_something(self):
        print("ConcreteStrategy2")

# Context
class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self):
        self.strategy.do_something()

# Usage example
if __name__ == "__main__":
    context = Context(ConcreteStrategy1())
    context.execute_strategy()  # Output: ConcreteStrategy1

    context = Context(ConcreteStrategy2())
    context.execute_strategy()  # Output: ConcreteStrategy2