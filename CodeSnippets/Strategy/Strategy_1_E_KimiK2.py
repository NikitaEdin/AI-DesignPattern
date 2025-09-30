from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def do(self, value): pass

class Add(Action):
    def do(self, value): return value + 1

class Multiply(Action):
    def do(self, value): return value * 2

class Square(Action):
    def do(self, value): return value ** 2

class Processor:
    def __init__(self, action): self.action = action
    def run(self, value): return self.action.do(value)

if __name__ == "__main__":
    tasks = [Add(), Multiply(), Square()]
    for task in tasks:
        print(Processor(task).run(5))