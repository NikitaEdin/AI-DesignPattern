from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import threading

class BehaviorProtocol(ABC):
    @abstractmethod
    def handle_request(self, context: 'MachineController', action: str, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def get_allowed_transitions(self) -> Dict[str, 'BehaviorProtocol']:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class IdleBehavior(BehaviorProtocol):
    def handle_request(self, context: 'MachineController', action: str, **kwargs) -> Any:
        if action == "start":
            return context.transition_to(ProcessingBehavior())
        elif action == "status":
            return "Machine is idle and ready"
        return f"Cannot {action} while idle"
    
    def get_allowed_transitions(self) -> Dict[str, BehaviorProtocol]:
        return {"processing": ProcessingBehavior()}
    
    def get_name(self) -> str:
        return "idle"

class ProcessingBehavior(BehaviorProtocol):
    def handle_request(self, context: 'MachineController', action: str, **kwargs) -> Any:
        if action == "pause":
            return context.transition_to(PausedBehavior())
        elif action == "stop":
            return context.transition_to(IdleBehavior())
        elif action == "complete":
            return context.transition_to(CompletedBehavior())
        elif action == "status":
            return "Machine is actively processing"
        return f"Cannot {action} while processing"
    
    def get_allowed_transitions(self) -> Dict[str, BehaviorProtocol]:
        return {
            "paused": PausedBehavior(),
            "idle": IdleBehavior(),
            "completed": CompletedBehavior()
        }
    
    def get_name(self) -> str:
        return "processing"

class PausedBehavior(BehaviorProtocol):
    def handle_request(self, context: 'MachineController', action: str, **kwargs) -> Any:
        if action == "resume":
            return context.transition_to(ProcessingBehavior())
        elif action == "stop":
            return context.transition_to(IdleBehavior())
        elif action == "status":
            return "Machine is paused"
        return f"Cannot {action} while paused"
    
    def get_allowed_transitions(self) -> Dict[str, BehaviorProtocol]:
        return {"processing": ProcessingBehavior(), "idle": IdleBehavior()}
    
    def get_name(self) -> str:
        return "paused"

class CompletedBehavior(BehaviorProtocol):
    def handle_request(self, context: 'MachineController', action: str, **kwargs) -> Any:
        if action == "reset":
            return context.transition_to(IdleBehavior())
        elif action == "status":
            return "Task completed successfully"
        return f"Cannot {action} when completed - reset first"
    
    def get_allowed_transitions(self) -> Dict[str, BehaviorProtocol]:
        return {"idle": IdleBehavior()}
    
    def get_name(self) -> str:
        return "completed"

class MachineController:
    def __init__(self):
        self._current_behavior: BehaviorProtocol = IdleBehavior()
        self._lock = threading.RLock()
        self._transition_history = []
    
    def transition_to(self, behavior: BehaviorProtocol) -> str:
        with self._lock:
            old_name = self._current_behavior.get_name()
            self._current_behavior = behavior
            new_name = behavior.get_name()
            self._transition_history.append((old_name, new_name))
            return f"Transitioned from {old_name} to {new_name}"
    
    def request(self, action: str, **kwargs) -> Any:
        with self._lock:
            return self._current_behavior.handle_request(self, action, **kwargs)
    
    def get_current_mode(self) -> str:
        return self._current_behavior.get_name()
    
    def get_available_transitions(self) -> list:
        return list(self._current_behavior.get_allowed_transitions().keys())
    
    def get_transition_history(self) -> list:
        return self._transition_history.copy()

if __name__ == "__main__":
    machine = MachineController()
    
    print(f"Initial mode: {machine.get_current_mode()}")
    print(machine.request("status"))
    
    print(machine.request("start"))
    print(f"Current mode: {machine.get_current_mode()}")
    print(f"Available transitions: {machine.get_available_transitions()}")
    
    print(machine.request("pause"))
    print(machine.request("resume"))
    print(machine.request("complete"))
    print(machine.request("reset"))
    
    print(f"Transition history: {machine.get_transition_history()}")