import threading
import weakref
from typing import Protocol, Set, Dict, Optional
from collections import defaultdict

class Alertable(Protocol):
    def on_notice(self, alert_id: str, severity: int) -> None: ...

class AlertHub:
    def __init__(self):
        self._watchers: Dict[int, Set[weakref.ref[Alertable]]] = defaultdict(set)
        self._lock = threading.RLock()
        self._failures: Dict[str, int] = {}
        self._failure_ids: Set[str] = set()
    
    def add_watcher(self, watcher: Alertable, priority: int = 0) -> 'AlertHub':
        with self._lock:
            self._watchers[priority].add(weakref.ref(watcher, self._cleanup_failures))
        return self
    
    def remove_watcher(self, watcher: Alertable) -> 'AlertHub':
        with self._lock:
            for priority in self._watchers:
                self._watchers[priority] = {ref for ref in self._watchers[priority] if ref() != watcher}
        return self
    
    def notify_for(self, alert_id: str, severity: int) -> None:
        watchers_copy: Set[weakref.ref[Alertable]] = set()
        with self._lock:
            for priority in sorted(self._watchers.keys(), reverse=True):
                watchers_copy.update(self._watchers[priority])
        
        for ref in watchers_copy:
            watcher = ref()
            if watcher:
                try:
                    watcher.on_notice(alert_id, severity)
                except Exception:
                    with self._lock:
                        self._failures[alert_id] = self._failures.get(alert_id, 0) + 1
                        self._failure_ids.add(alert_id)
    
    def _cleanup_failures(self, ref: weakref.ref) -> None:
        with self._lock:
            for priority in self._watchers:
                self._watchers[priority].discard(ref)
    
    def __iadd__(self, watcher: Alertable) -> 'AlertHub':
        self.add_watcher(watcher)
        return self
    
    def __isub__(self, watcher: Alertable) -> 'AlertHub':
        self.remove_watcher(watcher)
        return self

class ConsoleSink:
    def __init__(self):
        self.history: list[tuple[str, int]] = []
    
    def on_notice(self, alert_id: str, severity: int) -> None:
        self.history.append((alert_id, severity))
        print(f"Received alert {alert_id} at severity {severity}")

class Sensor:
    def __init__(self, hub: AlertHub):
        self._hub = hub
        self._running = False
    
    def start(self) -> None:
        self._running = True
    
    def stop(self) -> None:
        self._running = False
    
    def trigger(self, alert_id: str, severity: int) -> None:
        self._hub.notify_for(alert_id, severity)

if __name__ == "__main__":
    hub = AlertHub()
    sink1 = ConsoleSink()
    sink2 = ConsoleSink()
    
    hub += sink1
    hub += sink2
    
    sensor = Sensor(hub)
    sensor.start()
    sensor.trigger("ALERT123", 5)
    
    hub -= sink1
    sensor.trigger("ALERT456", 8)