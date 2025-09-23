```python
        class Strategy:
            def do_something(self):
                pass

        class ConcreteStrategyA(Strategy):
            def do_something(self):
                print("Concrete strategy A")

        class ConcreteStrategyB(Strategy):
            def do_something(self):
                print("Concrete strategy B")

        class Context:
            def __init__(self, strategy):
                self.strategy = strategy

            def do_something(self):
                return self.strategy.do_something()

        if __name__ == "__main__":
            context = Context(ConcreteStrategyA())
            print(context.do_something())  # Output: Concrete strategy A

            context = Context(ConcreteStrategyB())
            print(context.do_something())  # Output: Concrete strategy B
        ```