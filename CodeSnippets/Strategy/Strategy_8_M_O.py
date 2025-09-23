from abc import ABC, abstractmethod
import time

class OperationBase(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class AddOperation(OperationBase):
    def execute(self, a, b):
        return a + b

class MultiplyOperation(OperationBase):
    def execute(self, a, b):
        return a * b

class SafeDivideOperation(OperationBase):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

class Processor:
    def __init__(self, operation: OperationBase):
        if not isinstance(operation, OperationBase):
            raise TypeError("operation must implement OperationBase")
        self._operation = operation

    def set_operation(self, operation: OperationBase):
        if not isinstance(operation, OperationBase):
            raise TypeError("operation must implement OperationBase")
        self._operation = operation

    def perform(self, a, b):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("operands must be numbers")
        start = time.perf_counter()
        try:
            result = self._operation.execute(a, b)
        except Exception as exc:
            print(f"Operation failed: {exc}")
            return None
        duration = (time.perf_counter() - start) * 1000
        print(f"Executed in {duration:.3f} ms")
        return result

if __name__ == "__main__":
    adder = AddOperation()
    multiplier = MultiplyOperation()
    divider = SafeDivideOperation()

    processor = Processor(adder)
    print("Add:", processor.perform(10, 5))

    processor.set_operation(multiplier)
    print("Multiply:", processor.perform(10, 5))

    processor.set_operation(divider)
    print("Divide:", processor.perform(10, 2))
    print("Divide by zero attempt:", processor.perform(10, 0))

    try:
        processor.set_operation("not an operation")
    except TypeError as e:
        print("Failed to set operation:", e)