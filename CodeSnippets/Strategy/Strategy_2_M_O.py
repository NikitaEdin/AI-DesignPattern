from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, Tuple, Any


class OperationBase(ABC):
    @abstractmethod
    def apply(self, x: float, y: float) -> float:
        pass


class AddOperation(OperationBase):
    def apply(self, x: float, y: float) -> float:
        return x + y


class MultiplyOperation(OperationBase):
    def apply(self, x: float, y: float) -> float:
        return x * y


class PowerOperation(OperationBase):
    def apply(self, x: float, y: float) -> float:
        return x ** y


class Calculator:
    def __init__(self, operation: OperationBase, history_size: int = 10):
        self.set_operation(operation)
        self._history: Deque[Tuple[str, Any]] = deque(maxlen=history_size)

    def set_operation(self, operation: OperationBase):
        if not hasattr(operation, "apply") or not callable(getattr(operation, "apply")):
            raise TypeError("operation must provide an executable apply(x, y) method")
        self._operation = operation

    def compute(self, x: float, y: float) -> float:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("inputs must be numeric")
        try:
            result = self._operation.apply(x, y)
        except Exception as exc:
            raise RuntimeError(f"operation failed: {exc}") from exc
        self._history.append((self._operation.__class__.__name__, (x, y, result)))
        return result

    def get_history(self):
        return list(self._history)

    def clear_history(self):
        self._history.clear()


if __name__ == "__main__":
    calc = Calculator(AddOperation(), history_size=5)
    print(calc.compute(3, 4))
    calc.set_operation(MultiplyOperation())
    print(calc.compute(3, 4))
    calc.set_operation(PowerOperation())
    print(calc.compute(2, 8))
    for entry in calc.get_history():
        print(entry)