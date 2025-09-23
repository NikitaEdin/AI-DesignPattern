from abc import ABC, abstractmethod
from typing import Dict, Any
import threading

class BehaviorInterface(ABC):
    @abstractmethod
    def handle_request(self, context: 'Context', request: str) -> str:
        pass
    
    @abstractmethod
    def can_transition_to(self, target: str) -> bool:
        pass

class IdleBehavior(BehaviorInterface):
    def handle_request(self, context: 'Context', request: str) -> str:
        if request == "start":
            context.change_behavior("active")
            return "System activated"
        return "System is idle. Use 'start' to activate."
    
    def can_transition_to(self, target: str) -> bool:
        return target in ["active", "maintenance"]

class ActiveBehavior(BehaviorInterface):
    def handle_request(self, context: 'Context', request: str) -> str:
        if request == "stop":
            context.change_behavior("idle")
            return "System stopped"
        elif request == "error":
            context.change_behavior("error")
            return "Error occurred!"
        elif request == "process":
            return "Processing request..."
        return "System active. Commands: stop, error, process"
    
    def can_transition_to(self, target: str) -> bool:
        return target in ["idle", "error", "maintenance"]

class ErrorBehavior(BehaviorInterface):
    def handle_request(self, context: 'Context', request: str) -> str:
        if request == "reset":
            context.change_behavior("idle")
            return "System reset to idle"
        elif request == "diagnose":
            return "Running diagnostics..."
        return "System in error mode. Commands: reset, diagnose"
    
    def can_transition_to(self, target: str) -> bool:
        return target in ["idle", "maintenance"]

class MaintenanceBehavior(BehaviorInterface):
    def handle_request(self, context: 'Context', request: str) -> str:
        if request == "complete":
            context.change_behavior("idle")
            return "Maintenance complete"
        elif request == "update":
            return "Updating system..."
        return "System under maintenance. Commands: complete, update"
    
    def can_transition_to(self, target: str) -> bool:
        return target in ["idle"]

class Context:
    def __init__(self):
        self._behaviors: Dict[str, BehaviorInterface] = {
            "idle": IdleBehavior(),
            "active": ActiveBehavior(),
            "error": ErrorBehavior(),
            "maintenance": MaintenanceBehavior()
        }
        self._current_behavior = self._behaviors["idle"]
        self._current_name = "idle"
        self._lock = threading.Lock()
        self._transition_history = ["idle"]
    
    def change_behavior(self, behavior_name: str) -> bool:
        with self._lock:
            if behavior_name not in self._behaviors:
                return False
            
            if not self._current_behavior.can_transition_to(behavior_name):
                return False
            
            self._current_behavior = self._behaviors[behavior_name]
            self._current_name = behavior_name
            self._transition_history.append(behavior_name)
            return True
    
    def request(self, request: str) -> str:
        with self._lock:
            return self._current_behavior.handle_request(self, request)
    
    @property
    def current_mode(self) -> str:
        return self._current_name
    
    @property
    def history(self) -> list:
        return self._transition_history.copy()

if __name__ == "__main__":
    system = Context()
    
    commands = [
        "status", "start", "process", "error", 
        "diagnose", "reset", "start", "stop"
    ]
    
    for cmd in commands:
        result = system.request(cmd)
        print(f"Command: {cmd} | Mode: {system.current_mode} | Result: {result}")
    
    print(f"\nTransition History: {' -> '.join(system.history)}")