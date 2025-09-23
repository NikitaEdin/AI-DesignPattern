import abc
class Operation(abc.ABC):
    @abc.abstractmethod
    def execute(self, a, b): ...
class AddOperation(Operation):
    def execute(self, a, b): return a + b
class MultiplyOperation(Operation):
    def execute(self, a, b): return a * b
class Context:
    def __init__(self, operation): self.operation = operation
    def set_operation(self, operation): self.operation = operation
    def run(self, a, b): return self.operation.execute(a, b)
if __name__ == "__main__":
    ctx = Context(AddOperation())
    print(ctx.run(2, 3))
    ctx.set_operation(MultiplyOperation())
    print(ctx.run(2, 3))