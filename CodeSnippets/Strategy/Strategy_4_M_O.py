from abc import ABC, abstractmethod

class AlgorithmBase(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class AdditionAlgorithm(AlgorithmBase):
    def execute(self, a, b):
        return a + b

class MultiplicationAlgorithm(AlgorithmBase):
    def execute(self, a, b):
        return a * b

class FaultyAlgorithm(AlgorithmBase):
    def execute(self, a, b):
        raise RuntimeError("Intentional failure during execution")

class OperationContext:
    def __init__(self, algorithm: AlgorithmBase, fallback: AlgorithmBase = None):
        if not isinstance(algorithm, AlgorithmBase):
            raise TypeError("Primary algorithm must implement AlgorithmBase")
        if fallback is not None and not isinstance(fallback, AlgorithmBase):
            raise TypeError("Fallback algorithm must implement AlgorithmBase")
        self._algorithm = algorithm
        self._fallback = fallback

    def set_algorithm(self, algorithm: AlgorithmBase):
        if not isinstance(algorithm, AlgorithmBase):
            raise TypeError("New algorithm must implement AlgorithmBase")
        self._algorithm = algorithm

    def set_fallback(self, fallback: AlgorithmBase):
        if fallback is not None and not isinstance(fallback, AlgorithmBase):
            raise TypeError("Fallback algorithm must implement AlgorithmBase")
        self._fallback = fallback

    def process(self, a, b):
        try:
            return self._algorithm.execute(a, b)
        except Exception:
            if self._fallback is not None:
                try:
                    return self._fallback.execute(a, b)
                except Exception as exc:
                    raise RuntimeError("Both primary and fallback algorithms failed") from exc
            raise

if __name__ == "__main__":
    add = AdditionAlgorithm()
    mul = MultiplicationAlgorithm()
    faulty = FaultyAlgorithm()

    context = OperationContext(faulty, fallback=add)
    result1 = context.process(5, 3)
    print("Result with faulty primary (fallback add):", result1)

    context.set_algorithm(mul)
    result2 = context.process(5, 3)
    print("Result after swapping to multiply:", result2)

    context.set_fallback(None)
    context.set_algorithm(faulty)
    try:
        context.process(2, 2)
    except RuntimeError as e:
        print("Expected failure when no fallback is available:", str(e))