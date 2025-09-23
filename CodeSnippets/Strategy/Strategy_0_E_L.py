```python
        class Context:
            def __init__(self, strategy):
                self.strategy = strategy
            
            def execute(self):
                return self.strategy.do()
        
        class Strategy:
            def do(self):
                raise NotImplementedError("Do something!")
        
        class ConcreteStrategyA(Strategy):
            def do(self):
                return "ConcreteStrategyA does something!"
        
        class ConcreteStrategyB(Strategy):
            def do(self):
                return "ConcreteStrategyB does something!"
        
        if __name__ == '__main__':
            context = Context(ConcreteStrategyA())
            print(context.execute())
            
            context = Context(ConcreteStrategyB())
            print(context.execute())
        ```