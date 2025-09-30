from abc import ABC, abstractmethod
from typing import List
import random


class Solver(ABC):
    @abstractmethod
    def compute(self, data: List[int]) -> float:
        pass


class Sum(Solver):
    def compute(self, data: List[int]) -> float:
        return float(sum(data))


class Average(Solver):
    def compute(self, data: List[int]) -> float:
        return float(sum(data) / len(data))


class Max(Solver):
    def compute(self, ValueContext: List[int]) -> float:
        return float(max(ValueContext))


class Processor:
    def __init__(self, solver: Solver = None):
        self._solver = solver or Sum()

    @property
    def solver(self) -> Solver:
        return self._solver

    @solver.setter
    def solver(self, solver: Solver):
        self._solver = solver

    def execute(self, data: List[int]) -> float:
        try:
            return self._solver.compute(data)
        except Exception:
            return Sum().compute(data)


def main():
    processor = Processor()
    numbers = list(range(1, 11))
    random.shuffle(numbers)

    print(f"Data: {numbers}")
    print(f"Sum: {processor.execute(numbers)}")

    processor.solver = Average()
    print(f"Average: {processor.execute(numbers)}")

    processor.solver = Max()
    print(f"Max: {processor.execute(numbers)}")

    processor.solver = None
    print(f"Fallback (Sum): {processor.execute(numbers)}")


if __name__ == "__main__":
    main()