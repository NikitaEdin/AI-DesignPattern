from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class AddOperation(Operation):
    def execute(self, a, b):
        return a + b

class MultiplyOperation(Operation):
    def execute(self, a, b):
        return a * b

class Calculator:
    def __init__(self, policy):
        self.policy = policy
    def set_policy(self, policy):
        self.policy = policy
    def compute(self, a, b):
        return self.policy.execute(a, b)

if __name__ == "__main__":
    calc = Calculator(AddOperation())
    print(calc.compute(3, 4))
    calc.set_policy(MultiplyOperation())
    print(calc.compute(3, 4))