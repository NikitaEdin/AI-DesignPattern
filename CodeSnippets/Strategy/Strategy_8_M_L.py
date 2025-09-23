# A simple strategy design pattern implementation

class Strategy(object):
    def __init__(self, name):
        self.name = name

    def execute(self):
        print("Executing", self.name)


def main():
    # Create a context object that holds the current strategy
    context = Context()

    # Set the initial strategy to "strategy1"
    context.set_strategy(Strategy("strategy1"))

    # Execute the strategy
    context.execute()

    # Change the strategy to "strategy2"
    context.set_strategy(Strategy("strategy2"))

    # Execute the new strategy
    context.execute()

# A context class that holds a reference to the current strategy
class Context:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    def execute(self):
        return self._strategy.execute()