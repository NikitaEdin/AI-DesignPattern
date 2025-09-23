from abc import ABC, abstractmethod
class Action(ABC):
    @abstractmethod
    def run(self, a, b): pass
class AddAction(Action):
    def run(self, a, b): return a + b
class MultiplyAction(Action):
    def run(self, a, b): return a * b
class Calculator:
    def __init__(self, action: Action): self.action = action
    def set_action(self, action: Action): self.action = action
    def compute(self, a, b): return self.action.run(a, b)
def main():
    calc = Calculator(AddAction())
    print(calc.compute(3, 4))
    calc.set_action(MultiplyAction())
    print(calc.compute(3, 4))
if __name__ == "__main__":
    main()