import abc

class Algorithm(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def do_something(self):
        pass

class Strategy1(Algorithm):
    def do_something(self):
        print("Strategy 1")

class Strategy2(Algorithm):
    def do_something(self):
        print("Strategy 2")

class Context:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def execute_algorithm(self):
        self.algorithm.do_something()

if __name__ == "__main__":
    strategy1 = Strategy1()
    context = Context(strategy1)
    context.execute_algorithm()

    strategy2 = Strategy2()
    context.algorithm = strategy2
    context.execute_algorithm()