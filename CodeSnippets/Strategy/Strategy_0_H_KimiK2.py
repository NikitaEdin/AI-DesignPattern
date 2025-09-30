from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
from dataclasses import dataclass

@dataclass
class TaskData:
    items: List[Any]
    metadata: Dict[str, Any] = None

class ExecutionApproach(ABC):
    @abstractmethod
    def execute(self, data: TaskData) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def estimate_complexity(self, data: TaskData) -> float:
        pass

class BatchProcessor(ExecutionApproach):
    def execute(self, data: TaskData) -> Dict[str, Any]:
        start = time.time()
        processed = [item * 2 for item in data.items]
        duration = time.time() - start
        return {"processed": processed, "method": "batch", "time": duration}
    
    def estimate_complexity(self, data: TaskData) -> float:
        return len(data.items) * 0.1

class StreamProcessor(ExecutionApproach):
    def execute(self, data: TaskData) -> Dict[str, Any]:
        start = time.time()
        processed = []
        for item in data.items:
            time.sleep(0.01)
            processed.append(item * 2)
        duration = time.time() - start
        return {"processed": processed, "method": "stream", "time": duration}
    
    def estimate_complexity(self, data: TaskData) -> float:
        return len(data.items) * 0.5

class AdaptiveSelector(ExecutionApproach):
    def __init__(self, threshold: float = 50):
        self.threshold = threshold
        self.batch = BatchProcessor()
        self.stream = StreamProcessor()
    
    def execute(self, data: TaskData) -> Dict[str, Any]:
        complexity = self.estimate_complexity(data)
        chosen = self.batch if complexity < self.threshold else self.stream
        return chosen.execute(data)
    
    def estimate_complexity(self, data: TaskData) -> float:
        return len(data.items) * 0.25

class ProcessingContext:
    def __init__(self, initial_approach: ExecutionApproach):
        self._current = initial_approach
        self._history = []
    
    def set_approach(self, new_approach: ExecutionApproach) -> None:
        self._current = new_approach
    
    def process(self, data: TaskData) -> Dict[str, Any]:
        result = self._current.execute(data)
        self._history.append(result)
        return result
    
    def get_history(self) -> List[Dict[str, Any]]:
        return self._history

if __name__ == "__main__":
    data_small = TaskData(items=list(range(5)), metadata={"type": "test"})
    data_large = TaskData(items=list(range(100)), metadata={"type": "production"})
    
    context = ProcessingContext(AdaptiveSelector(threshold=30))
    
    print(context.process(data_small))
    context.set_approach(BatchProcessor())
    print(context.process(data_large))
    context.set_approach(StreamProcessor())
    print(context.process(data_small))