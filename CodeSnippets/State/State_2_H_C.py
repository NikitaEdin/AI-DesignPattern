from abc import ABC, abstractmethod
from typing import Dict, Any
import threading

class BehaviorContext(ABC):
    @abstractmethod
    def transition_to(self, new_behavior: 'Behavior') -> None:
        pass
    
    @abstractmethod
    def get_context_data(self) -> Dict[str, Any]:
        pass

class Behavior(ABC):
    def __init__(self):
        self._context: BehaviorContext = None
    
    @property
    def context(self) -> BehaviorContext:
        return self._context
    
    @context.setter
    def context(self, context: BehaviorContext) -> None:
        self._context = context
    
    @abstractmethod
    def handle_request(self, action: str) -> str:
        pass
    
    @abstractmethod
    def can_transition_to(self, target_behavior: str) -> bool:
        pass

class IdleBehavior(Behavior):
    def handle_request(self, action: str) -> str:
        if action == "start":
            self.context.transition_to(ProcessingBehavior())
            return "Starting processing"
        elif action == "shutdown":
            self.context.transition_to(OfflineBehavior())
            return "Shutting down"
        return "Cannot perform action while idle"
    
    def can_transition_to(self, target_behavior: str) -> bool:
        return target_behavior in ["processing", "offline"]

class ProcessingBehavior(Behavior):
    def handle_request(self, action: str) -> str:
        if action == "pause":
            self.context.transition_to(PausedBehavior())
            return "Processing paused"
        elif action == "complete":
            self.context.transition_to(IdleBehavior())
            return "Processing completed"
        elif action == "error":
            self.context.transition_to(ErrorBehavior())
            return "Error occurred during processing"
        return "Cannot perform action while processing"
    
    def can_transition_to(self, target_behavior: str) -> bool:
        return target_behavior in ["paused", "idle", "error"]

class PausedBehavior(Behavior):
    def handle_request(self, action: str) -> str:
        if action == "resume":
            self.context.transition_to(ProcessingBehavior())
            return "Processing resumed"
        elif action == "cancel":
            self.context.transition_to(IdleBehavior())
            return "Processing cancelled"
        return "Cannot perform action while paused"
    
    def can_transition_to(self, target_behavior: str) -> bool:
        return target_behavior in ["processing", "idle"]

class ErrorBehavior(Behavior):
    def handle_request(self, action: str) -> str:
        if action == "reset":
            self.context.transition_to(IdleBehavior())
            return "System reset from error"
        return "System in error - reset required"
    
    def can_transition_to(self, target_behavior: str) -> bool:
        return target_behavior in ["idle"]

class OfflineBehavior(Behavior):
    def handle_request(self, action: str) -> str:
        if action == "startup":
            self.context.transition_to(IdleBehavior())
            return "System started"
        return "System offline"
    
    def can_transition_to(self, target_behavior: str) -> bool:
        return target_behavior in ["idle"]

class WorkflowManager(BehaviorContext):
    def __init__(self):
        self._current_behavior: Behavior = IdleBehavior()
        self._current_behavior.context = self
        self._data: Dict[str, Any] = {"task_count": 0, "errors": 0}
        self._lock = threading.Lock()
        self._observers = []
    
    def transition_to(self, new_behavior: Behavior) -> None:
        with self._lock:
            old_behavior_name = type(self._current_behavior).__name__
            if self._current_behavior.can_transition_to(type(new_behavior).__name__.replace("Behavior", "").lower()):
                self._current_behavior = new_behavior
                self._current_behavior.context = self
                self._notify_observers(old_behavior_name, type(new_behavior).__name__)
            else:
                raise ValueError(f"Invalid transition from {old_behavior_name} to {type(new_behavior).__name__}")
    
    def process_action(self, action: str) -> str:
        with self._lock:
            result = self._current_behavior.handle_request(action)
            if action in ["complete", "error"]:
                self._data["task_count"] += 1
                if action == "error":
                    self._data["errors"] += 1
            return result
    
    def get_context_data(self) -> Dict[str, Any]:
        return self._data.copy()
    
    def current_mode(self) -> str:
        return type(self._current_behavior).__name__.replace("Behavior", "")
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def _notify_observers(self, old_mode: str, new_mode: str):
        for observer in self._observers:
            observer(old_mode, new_mode)

if __name__ == "__main__":
    def mode_changed(old_mode: str, new_mode: str):
        print(f"Transitioned: {old_mode} -> {new_mode}")
    
    manager = WorkflowManager()
    manager.add_observer(mode_changed)
    
    actions = ["start", "pause", "resume", "complete", "start", "error", "reset", "shutdown", "startup"]
    
    for action in actions:
        try:
            result = manager.process_action(action)
            print(f"Action '{action}': {result} | Mode: {manager.current_mode()}")
        except ValueError as e:
            print(f"Action '{action}': {e}")
    
    print(f"Final context data: {manager.get_context_data()}")