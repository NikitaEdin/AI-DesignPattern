from abc import ABC, abstractmethod
from typing import Dict, Any
import threading

class Context:
    def __init__(self):
        self._current_mode = IdleMode()
        self._history = []
        self._lock = threading.Lock()
        self._listeners = []
    
    def add_listener(self, listener):
        self._listeners.append(listener)
    
    def _notify_listeners(self, event_data):
        for listener in self._listeners:
            listener(event_data)
    
    def transition_to(self, new_mode):
        with self._lock:
            old_mode = self._current_mode
            self._current_mode = new_mode
            self._current_mode.set_context(self)
            
            transition_data = {
                'from': old_mode.__class__.__name__,
                'to': new_mode.__class__.__name__,
                'timestamp': id(self)
            }
            self._history.append(transition_data)
            self._notify_listeners(transition_data)
    
    def handle_request(self, action: str, **kwargs) -> Any:
        with self._lock:
            return self._current_mode.handle(action, **kwargs)
    
    def get_current_mode(self) -> str:
        return self._current_mode.__class__.__name__
    
    def get_history(self) -> list:
        return self._history.copy()

class ModeBase(ABC):
    def __init__(self):
        self._context = None
    
    def set_context(self, context: Context):
        self._context = context
    
    @abstractmethod
    def handle(self, action: str, **kwargs) -> Any:
        pass
    
    def _invalid_action(self, action: str) -> str:
        return f"Action '{action}' not allowed in {self.__class__.__name__}"

class IdleMode(ModeBase):
    def handle(self, action: str, **kwargs) -> Any:
        if action == "start":
            self._context.transition_to(ActiveMode())
            return "System activated"
        elif action == "configure":
            self._context.transition_to(ConfigurationMode())
            return "Entering configuration"
        elif action == "status":
            return "System is idle"
        return self._invalid_action(action)

class ActiveMode(ModeBase):
    def __init__(self):
        super().__init__()
        self._operations_count = 0
    
    def handle(self, action: str, **kwargs) -> Any:
        if action == "process":
            self._operations_count += 1
            data = kwargs.get('data', 'default')
            if self._operations_count >= 5:
                self._context.transition_to(OverloadMode())
                return f"Processing {data} - System overloaded"
            return f"Processing {data} - Operation #{self._operations_count}"
        elif action == "stop":
            self._context.transition_to(IdleMode())
            return "System stopped"
        elif action == "status":
            return f"System active - {self._operations_count} operations performed"
        return self._invalid_action(action)

class ConfigurationMode(ModeBase):
    def __init__(self):
        super().__init__()
        self._settings = {}
    
    def handle(self, action: str, **kwargs) -> Any:
        if action == "set":
            key, value = kwargs.get('key'), kwargs.get('value')
            if key and value is not None:
                self._settings[key] = value
                return f"Setting {key} = {value}"
            return "Invalid configuration parameters"
        elif action == "apply":
            self._context.transition_to(IdleMode())
            return f"Configuration applied: {self._settings}"
        elif action == "status":
            return f"Configuring - Current settings: {self._settings}"
        return self._invalid_action(action)

class OverloadMode(ModeBase):
    def handle(self, action: str, **kwargs) -> Any:
        if action == "reset":
            self._context.transition_to(IdleMode())
            return "System reset to idle"
        elif action == "emergency_stop":
            self._context.transition_to(IdleMode())
            return "Emergency stop executed"
        elif action == "status":
            return "System overloaded - limited operations available"
        return self._invalid_action(action)

if __name__ == "__main__":
    def event_logger(event):
        print(f"Transition: {event['from']} -> {event['to']}")
    
    system = Context()
    system.add_listener(event_logger)
    
    print(system.handle_request("status"))
    print(system.handle_request("start"))
    print(system.handle_request("process", data="task1"))
    print(system.handle_request("process", data="task2"))
    print(system.handle_request("process", data="task3"))
    print(system.handle_request("process", data="task4"))
    print(system.handle_request("process", data="task5"))
    print(system.handle_request("reset"))
    print(system.handle_request("configure"))
    print(system.handle_request("set", key="timeout", value=30))
    print(system.handle_request("apply"))
    
    print(f"\nFinal mode: {system.get_current_mode()}")
    print(f"History: {len(system.get_history())} transitions")