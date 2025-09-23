import threading
import weakref
from typing import Any, Callable, Dict, List
from abc import ABC, abstractmethod

class StateManager:
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._watchers: Dict[int, weakref.ReferenceType[StateWatcher]] = {}
        self._next_priority: int = 0
        self._lock: threading.Lock = threading.Lock()

    def attach_watcher(self, watcher: 'StateWatcher', priority: int = 0) -> None:
        with self._lock:
            if priority in self._watchers:
                raise ValueError("Priority already in use")
            self._watchers[priority] = weakref.ref(watcher)
            self._next_priority = max(self._next_priority, priority + 1)

    def detach_watcher(self, watcher: 'StateWatcher') -> None:
        with self._lock:
            for priority, ref in list(self._watchers.items()):
                if ref() is watcher:
                    del self._watchers[priority]
                    break

    def set_state(self, key: str, value: Any) -> None:
        with self._lock:
            self._state[key] = value
        self._notify_watchers(key, value)

    def _notify_watchers(self, key: str, value: Any) -> None:
        with self._lock:
            active_watchers = [(p, ref()) for p, ref in self._watchers.items() if ref() is not None]
        for priority, watcher in sorted(active_watchers, reverse=True):
            if watcher:
                try:
                    watcher.handle_update(key, value)
                except Exception:
                    pass  # Ignore errors from individual watchers

class StateWatcher(ABC):
    @abstractmethod
    def handle_update(self, key: str, value: Any) -> None:
        pass

class TemperatureMonitor(StateWatcher):
    def __init__(self, name: str):
        self.name = name

    def handle_update(self, key: str, value: Any) -> None:
        if key == "temperature":
            print(f"{self.name} received temperature: {value}")

class AlertSystem(StateWatcher):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def handle_update(self, key: str, value: Any) -> None:
        if key == "temperature" and value > self.threshold:
            print(f"Alert: Temperature {value} exceeds threshold {self.threshold}")

if __name__ == "__main__":
    manager = StateManager()
    monitor1 = TemperatureMonitor("Sensor A")
    monitor2 = TemperatureMonitor("Sensor B")
    alert = AlertSystem(30.0)

    manager.attach_watcher(monitor1, priority=1)
    manager.attach_watcher(monitor2, priority=2)
    manager.attach_watcher(alert, priority=0)

    manager.set_state("temperature", 25.0)
    manager.set_state("temperature", 35.0)

    manager.detach_watcher(monitor1)
    manager.set_state("temperature", 40.0)