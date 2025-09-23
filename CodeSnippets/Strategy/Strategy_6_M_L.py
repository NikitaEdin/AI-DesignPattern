class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def execute(self):
        return self.strategy.do_something()

class ConcreteStrategyA:
    def do_something(self):
        print("Strategy A")

class ConcreteStrategyB:
    def do_something(self):
        print("Strategy B")

if __name__ == "__main__":
    context = Context(ConcreteStrategyA())
    result = context.execute()
    print(result)