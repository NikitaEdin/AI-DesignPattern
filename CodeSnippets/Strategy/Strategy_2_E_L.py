class Context(object):
    def __init__(self, strategy):
        self._strategy = strategy
    
    def execute(self, *args, **kwargs):
        return self._strategy.do_something(*args, **kwargs)


class ConcreteStrategyA(object):
    def do_something(self, arg1, arg2):
        return arg1 + arg2


class ConcreteStrategyB(object):
    def do_something(self, arg1, arg2):
        return arg1 - arg2


if __name__ == "__main__":
    context = Context(ConcreteStrategyA())
    result = context.execute(3, 5)
    print(result) # prints 8
    
    context = Context(ConcreteStrategyB())
    result = context.execute(3, 5)
    print(result) # prints -2