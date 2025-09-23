from abc import ABC, abstractmethod
from typing import Dict, Any
import functools

def transition_guard(allowed_from=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if allowed_from and self.context._current_mode.__class__.__name__ not in allowed_from:
                raise RuntimeError(f"Invalid transition from {self.context._current_mode.__class__.__name__}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class ModeContext:
    def __init__(self):
        self._current_mode = None
        self._history = []
        self._data = {}
        
    def set_mode(self, mode):
        if self._current_mode:
            self._history.append(self._current_mode.__class__.__name__)
            self._current_mode.exit(self)
        self._current_mode = mode
        self._current_mode.enter(self)
        
    def revert_to_previous(self):
        if self._history:
            previous_name = self._history.pop()
            mode_class = globals()[previous_name]
            self.set_mode(mode_class())
            
    def store_data(self, key: str, value: Any):
        self._data[key] = value
        
    def get_data(self, key: str, default=None):
        return self._data.get(key, default)
        
    def execute_action(self, action: str, *args, **kwargs):
        return self._current_mode.handle_action(action, self, *args, **kwargs)

class OperationMode(ABC):
    @abstractmethod
    def enter(self, context: ModeContext):
        pass
        
    @abstractmethod
    def exit(self, context: ModeContext):
        pass
        
    @abstractmethod
    def handle_action(self, action: str, context: ModeContext, *args, **kwargs):
        pass

class IdleMode(OperationMode):
    def enter(self, context: ModeContext):
        context.store_data("idle_entry_time", "00:00")
        
    def exit(self, context: ModeContext):
        context.store_data("last_idle_duration", "calculated_time")
        
    @transition_guard(allowed_from=["ActiveMode", "MaintenanceMode"])
    def handle_action(self, action: str, context: ModeContext, *args, **kwargs):
        if action == "activate":
            context.set_mode(ActiveMode())
            return "Transitioning to active"
        elif action == "maintain":
            context.set_mode(MaintenanceMode())
            return "Entering maintenance"
        return "Idling..."

class ActiveMode(OperationMode):
    def enter(self, context: ModeContext):
        context.store_data("active_tasks", [])
        
    def exit(self, context: ModeContext):
        tasks = context.get_data("active_tasks", [])
        context.store_data("completed_tasks", len(tasks))
        
    def handle_action(self, action: str, context: ModeContext, *args, **kwargs):
        if action == "process":
            tasks = context.get_data("active_tasks", [])
            task = kwargs.get("task", "default_task")
            tasks.append(task)
            context.store_data("active_tasks", tasks)
            return f"Processing {task}"
        elif action == "complete":
            context.set_mode(IdleMode())
            return "Work completed"
        elif action == "error":
            context.set_mode(ErrorMode())
            return "Error encountered"
        return "Working..."

class ErrorMode(OperationMode):
    def enter(self, context: ModeContext):
        context.store_data("error_count", context.get_data("error_count", 0) + 1)
        
    def exit(self, context: ModeContext):
        context.store_data("last_error_resolved", True)
        
    def handle_action(self, action: str, context: ModeContext, *args, **kwargs):
        if action == "recover":
            context.revert_to_previous()
            return "Recovered from error"
        elif action == "reset":
            context.set_mode(IdleMode())
            return "System reset"
        return "Error mode active"

class MaintenanceMode(OperationMode):
    def enter(self, context: ModeContext):
        context.store_data("maintenance_tasks", ["check_1", "check_2"])
        
    def exit(self, context: ModeContext):
        context.store_data("last_maintenance", "completed")
        
    @transition_guard(allowed_from=["IdleMode"])
    def handle_action(self, action: str, context: ModeContext, *args, **kwargs):
        if action == "finish":
            context.set_mode(IdleMode())
            return "Maintenance completed"
        return "Performing maintenance"

if __name__ == "__main__":
    system = ModeContext()
    system.set_mode(IdleMode())
    
    print(system.execute_action("activate"))
    print(system.execute_action("process", task="critical_job"))
    print(system.execute_action("error"))
    print(system.execute_action("recover"))
    print(system.execute_action("complete"))
    print(system.execute_action("maintain"))
    print(system.execute_action("finish"))