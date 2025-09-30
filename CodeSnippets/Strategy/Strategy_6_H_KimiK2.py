from abc import ABC, abstractmethod
from typing import List, Any, Optional
import random
import time
from dataclasses import dataclass

class ScoringMethod(ABC):
    @abstractmethod
    def evaluate(self, data: List[Any]) -> float: ...

class SpeedScoring(ScoringMethod):
    def evaluate(self, data: List[float]) -> float:
        if not data: raise ValueError("Empty dataset")
        return round(sum(data) / len(data), 2) + random.uniform(0, 0.001)

class PrecisionScoring(ScoringMethod):
    def evaluate(self, data: List[float]) -> float:
        if not data: raise ValueError("Empty dataset")
        return round(sum(data) / len(data), 6)

class AdaptiveScoring(ScoringMethod):
    def __init__(self):
        self._cache = {}
        self._hits = 0
    
    def evaluate(self, data: List[float]) -> float:
        key = tuple(data)
        if key in self._cache: 
            self._hits += 1
            return self._cache[key]
        score = round(sum(data) / len(data), 4)
        self._cache[key] = score
        return score

class Evaluator:
    def __init__(self, method: Optional[ScoringMethod] = None):
        self.method = method
    
    def compute_score(self, data: List[float]) -> float:
        if not self.method:
            raise RuntimeError("No scoring method set")
        return self.method.evaluate(data)
    
    def change_method(self, method: ScoringMethod):
        self.method = method

class DynamicEvaluator(Evaluator):
    def __init__(self):
        self.history = []
        super().__init__(AdaptiveScoring())
    
    def compute_score(self, data: List[float]) -> float:
        self.history.append(time.time())
        return super().compute_score(data)
    
    def auto_switch(self):
        if len(self.history) > 10:
            self.history.pop(0)
        if len(self.history) == 10:
            avg_gap = sum(self.history[i] - self.history[i-1] for i in range(1, 10))/9
            self.method = PrecisionScoring() if avg_gap > 1 else SpeedScoring()

if __name__ == "__main__":
    evaluator = DynamicEvaluator()
    for i in range(20):
        score = evaluator.compute_score([1, 2, 3])
        print(round(score, 3))
        evaluator.auto_switch()
        time.sleep(0.1)