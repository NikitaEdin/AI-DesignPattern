class Context(object):
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_strategy(self):
        return self.strategy.do_something()

class StrategyA(object):
    def do_something(self):
        return "Result A"

class StrategyB(object):
    def do_something(self):
        return "Result B"

if __name__ == '__main__':
    context = Context(StrategyA())
    result = context.execute_strategy()
    print(result) # Output: Result A

    context = Context(StrategyB())
    result = context.execute_strategy()
    print(result) # Output: Result B