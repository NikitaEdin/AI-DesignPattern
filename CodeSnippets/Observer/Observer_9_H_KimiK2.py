from __future__ import annotations
from typing import Set, Dict, Any, Callable, List
import weakref
import threading

class _WeakCallable:
    def __init__(self, target: Callable):
        try:
            self._obj = weakref.ref(target.__self__)
            self._func = target.__func__
        except AttributeError:
            self._obj = None
            self._func = target
    def __call__(self, *args, **kwargs):
        obj = self._obj() if self._obj else None
        if obj is not None:
            return self._func(obj, *args, **kwargs)
        elif self._obj is None:
            return self._func(*args, **kwargs)
    def __hash__(self):
        return hash((self._obj, self._func))
    def __eq__(self, other):
        return hash(self) == hash(other)

class Dispatcher:
    _lock = threading.RLock()
    _topics: Dict[str, Set[_WeakCallable]] = {}

    @classmethod
    def attach(cls, topic: str, callback: Callable[[Any, ...], None]) -> None:
        with cls._lock:
            cls._topics.setdefault(topic, set())
            cls._topics[topic].add(_WeakCallable(callback))
            cls._topics[topic] = {c for c in cls._topics[topic] if c._obj is None or c._obj() is not None}

    @classmethod
    def detach(cls, topic: str, callback: Callable) -> None:
        with cls._lock:
            if topic in cls._topics:
                cls._topics[topic].discard(_WeakCallable(callback))

    @classmethod
    def emit(cls, topic: str, payload: Any = None) -> None:
        with cls._lock:
            dead = set()
            for handler in cls._topics.get(topic, set()):
                try:
                    handler(payload)
                except ReferenceError:
                    dead.add(handler)
            cls._topics[topic] -= dead

class Sensor:
    def __init__(self, name: str):
        self.name = name
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        Dispatcher.emit(f"{self.name}:update", {"name": self.name, "new": v, "old": self._value})

class Logger:
    def __init__(self, ident: str):
        self.ident = ident
    def log(self, data):
        print(f"[{self.ident}] {data['name']} changed to {data['new']}")

class Alert:
    def __init__(self, threshold: int):
        self.threshold = threshold
    def check(self, data):
        if data['new'] > self.threshold:
            print(f"⚠️  Alert from {data['name']}: {data['new']} exceeds {self.threshold}")

if __name__ == "__main__":
    t = Sensor("temperature")
    h = Sensor("humidity")
    log = Logger("main")
    alert = Alert(30)
    Dispatcher.attach("temperature:update", log.log)
    Dispatcher.attach("temperature:update", alert.check)
    Dispatcher.attach("humidity:update", log.log)
    t.value = 25
    h.value = 70
    t.value = 35
    Dispatcher.detach("temperature:update", alert.check)
    t.value = 40