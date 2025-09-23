class Context:
    def __init__(self, strategy):
        self._strategy = strategy
    
    def execute(self, x, y):
        return self._strategy.do_something(x, y)

class Strategy1:
    def do_something(self, x, y):
        return x + y

class Strategy2:
    def do_something(self, x, y):
        return x - y

def main():
    context = Context(Strategy1())
    result = context.execute(3, 5)
    print(result) # prints 8
    
    context = Context(Strategy2())
    result = context.execute(3, 5)
    print(result) # prints -2