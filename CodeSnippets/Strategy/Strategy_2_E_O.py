class Operation:
    def execute(self, a, b):
        raise NotImplementedError

class Add(Operation):
    def execute(self, a, b):
        return a + b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Context:
    def __init__(self, operation: Operation):
        self.operation = operation
    def set_operation(self, operation: Operation):
        self.operation = operation
    def run(self, a, b):
        return self.operation.execute(a, b)

if __name__ == "__main__":
    ctx = Context(Add())
    print("Add:", ctx.run(3, 4))
    ctx.set_operation(Multiply())
    print("Multiply:", ctx.run(3, 4))