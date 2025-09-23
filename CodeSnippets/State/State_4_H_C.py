from abc import ABC, abstractmethod
from typing import Dict, Any
import threading

class Condition(ABC):
    @abstractmethod
    def handle_request(self, context: 'Context', action: str, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def can_transition_to(self, target: 'Condition') -> bool:
        pass

class IdleCondition(Condition):
    def handle_request(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == "start":
            context.transition_to(ProcessingCondition())
            return "Starting process"
        return "Invalid action in idle mode"
    
    def can_transition_to(self, target: 'Condition') -> bool:
        return isinstance(target, (ProcessingCondition, ErrorCondition))

class ProcessingCondition(Condition):
    def handle_request(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == "complete":
            context.transition_to(CompletedCondition())
            return "Process completed"
        elif action == "pause":
            context.transition_to(PausedCondition())
            return "Process paused"
        elif action == "error":
            context.transition_to(ErrorCondition())
            return "Process encountered error"
        return "Invalid action during processing"
    
    def can_transition_to(self, target: 'Condition') -> bool:
        return isinstance(target, (CompletedCondition, PausedCondition, ErrorCondition))

class PausedCondition(Condition):
    def handle_request(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == "resume":
            context.transition_to(ProcessingCondition())
            return "Process resumed"
        elif action == "stop":
            context.transition_to(IdleCondition())
            return "Process stopped"
        return "Invalid action while paused"
    
    def can_transition_to(self, target: 'Condition') -> bool:
        return isinstance(target, (ProcessingCondition, IdleCondition))

class CompletedCondition(Condition):
    def handle_request(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == "reset":
            context.transition_to(IdleCondition())
            return "Process reset to idle"
        return "Process is completed. Use 'reset' to restart"
    
    def can_transition_to(self, target: 'Condition') -> bool:
        return isinstance(target, IdleCondition)

class ErrorCondition(Condition):
    def handle_request(self, context: 'Context', action: str, **kwargs) -> Any:
        if action == "retry":
            context.transition_to(ProcessingCondition())
            return "Retrying process"
        elif action == "reset":
            context.transition_to(IdleCondition())
            return "Reset to idle after error"
        return "Error occurred. Use 'retry' or 'reset'"
    
    def can_transition_to(self, target: 'Condition') -> bool:
        return isinstance(target, (ProcessingCondition, IdleCondition))

class Context:
    def __init__(self):
        self._current_condition = IdleCondition()
        self._lock = threading.RLock()
        self._history = []
    
    def transition_to(self, condition: Condition):
        with self._lock:
            if self._current_condition.can_transition_to(condition):
                old_condition = type(self._current_condition).__name__
                self._current_condition = condition
                new_condition = type(self._current_condition).__name__
                self._history.append((old_condition, new_condition))
            else:
                raise ValueError(f"Invalid transition from {type(self._current_condition).__name__} to {type(condition).__name__}")
    
    def request(self, action: str, **kwargs) -> Any:
        with self._lock:
            return self._current_condition.handle_request(self, action, **kwargs)
    
    @property
    def current_mode(self) -> str:
        return type(self._current_condition).__name__
    
    @property
    def transition_history(self) -> list:
        return self._history.copy()

if __name__ == "__main__":
    processor = Context()
    
    actions = ["start", "pause", "resume", "complete", "reset", "start", "error", "retry", "complete"]
    
    for action in actions:
        try:
            result = processor.request(action)
            print(f"Action: {action} -> {result} | Mode: {processor.current_mode}")
        except Exception as e:
            print(f"Action: {action} -> Error: {e}")
    
    print(f"\nTransition History: {processor.transition_history}")