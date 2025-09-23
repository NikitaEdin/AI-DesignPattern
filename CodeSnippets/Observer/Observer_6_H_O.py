import threading
import weakref
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Dict, List

@dataclass(order=True)
class Subscription:
    priority: int
    created: float = field(compare=False)
    id: int = field(compare=False)
    ref: Any = field(compare=False)
    event_type: Optional[str] = field(compare=False)
    predicate: Optional[Callable[[str, Any], bool]] = field(compare=False)
    one_shot: bool = field(compare=False)

class Subject:
    def __init__(self):
        self._lock = threading.RLock()
        self._subs: Dict[int, Subscription] = {}
        self._counter = 0

    def _make_ref(self, callback):
        if hasattr(callback, "__self__") and hasattr(callback, "__func__"):
            return weakref.WeakMethod(callback)
        try:
            return weakref.ref(callback)
        except TypeError:
            return lambda: callback

    def subscribe(self, callback: Callable, event_type: Optional[str] = None,
                  predicate: Optional[Callable[[str, Any], bool]] = None,
                  one_shot: bool = False, priority: int = 0) -> int:
        with self._lock:
            self._counter += 1
            token = self._counter
            ref = self._make_ref(callback)
            sub = Subscription(priority=-priority, created=time.time(), id=token,
                               ref=ref, event_type=event_type,
                               predicate=predicate, one_shot=one_shot)
            self._subs[token] = sub
            return token

    def unsubscribe(self, token_or_callback):
        with self._lock:
            if isinstance(token_or_callback, int):
                self._subs.pop(token_or_callback, None)
                return
            to_remove = []
            for tid, sub in self._subs.items():
                cb = self._deref(sub.ref)
                if cb is None:
                    to_remove.append(tid)
                elif cb == token_or_callback:
                    to_remove.append(tid)
            for tid in to_remove:
                self._subs.pop(tid, None)

    def _deref(self, ref):
        try:
            return ref()
        except Exception:
            return None

    def notify(self, event_type: str, data: Any = None, stop_on_exception: bool = False) -> List[Exception]:
        exceptions: List[Exception] = []
        to_remove: List[int] = []
        with self._lock:
            candidates = sorted(self._subs.values())
        for sub in candidates:
            cb = self._deref(sub.ref)
            if cb is None:
                to_remove.append(sub.id)
                continue
            if sub.event_type is not None and sub.event_type != event_type:
                continue
            try:
                if sub.predicate and not sub.predicate(event_type, data):
                    continue
                cb(event_type, data)
                if sub.one_shot:
                    to_remove.append(sub.id)
            except Exception as exc:
                exceptions.append(exc)
                if stop_on_exception:
                    break
        if to_remove:
            with self._lock:
                for tid in to_remove:
                    self._subs.pop(tid, None)
        return exceptions

if __name__ == "__main__":
    bus = Subject()

    class Printer:
        def __init__(self, name):
            self.name = name
        def handle(self, event, payload):
            print(f"{self.name} received {event}: {payload}")

    def free_func(event, payload):
        print(f"free_func received {event}: {payload}")

    p1 = Printer("A")
    p2 = Printer("B")

    t1 = bus.subscribe(p1.handle, priority=10)
    t2 = bus.subscribe(p2.handle, event_type="update", priority=5)
    t3 = bus.subscribe(free_func, predicate=lambda e, d: isinstance(d, dict))
    t4 = bus.subscribe(lambda e, d: print("one-shot got", e, d), one_shot=True)

    print("Notify 'update' with dict:")
    bus.notify("update", {"k": "v"})

    print("Notify 'create' with string:")
    bus.notify("create", "payload")

    bus.unsubscribe(t1)
    print("After unsubscribing A, notify 'update':")
    bus.notify("update", {"another": 1})