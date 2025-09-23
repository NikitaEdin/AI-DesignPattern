```python
class Context(object):
    def __init__(self, strategy):
        self._strategy = strategy
    
    def do_something(self):
        return self._strategy.do_something()
    
    def do_something_else(self):
        return self._strategy.do_something_else()

class ConcreteStrategyA(object):
    def do_something(self):
        return "This is the result of doing something with A"
    
    def do_something_else(self):
        return "This is the result of doing something else with A"

class ConcreteStrategyB(object):
    def do_something(self):
        return "This is the result of doing something with B"
    
    def do_something_else(self):
        return "This is the result of doing something else with B"

if __name__ == "__main__":
    context = Context(ConcreteStrategyA())
    print(context.do_something())
    print(context.do_something_else())

    context = Context(ConcreteStrategyB())
    print(context.do_something())
    print(context.do_something_else())
  ```