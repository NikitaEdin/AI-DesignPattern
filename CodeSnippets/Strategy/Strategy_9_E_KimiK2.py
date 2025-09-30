class Operation:
    def execute(self, a, b):
        pass

class Add(Operation):
    def execute(self, a, b):
        return a + b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Context:
    def __init__(self, operation):
        self.operation = operation
    def perform(self, a, b):
        return self.operation.execute(a, b)

if __name__ == "__main__":
    c = Context(Add())
    print(c.perform(3, 4))
    c = Context(Multiply())
    print(c.perform(3, 4))