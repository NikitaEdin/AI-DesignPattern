from dataclasses import dataclass
from typing import Callable, Optional, Any
import threading

@dataclass
class _Subscription:
    callback: Callable
    func: Any
    inst: Any
    priority: int
    filter_fn: Optional[Callable] = None

    def matches(self, other):
        func = getattr(other, "__func__", other)
        inst = getattr(other, "__self__", None)
        return func is self.func and inst is self.inst

class Notifier:
    def __init__(self):
        self._lock = threading.RLock()
        self._subs: list[_Subscription] = []
        self.last_message = None

    def subscribe(self, callback: Callable, priority: int = 0, filter_fn: Optional[Callable] = None):
        if not callable(callback):
            raise TypeError("callback must be callable")
        if filter_fn is not None and not callable(filter_fn):
            raise TypeError("filter_fn must be callable or None")
        func = getattr(callback, "__func__", callback)
        inst = getattr(callback, "__self__", None)
        with self._lock:
            for s in self._subs:
                if s.func is func and s.inst is inst and s.filter_fn == filter_fn:
                    return s  # avoid duplicate identical subscription
            sub = _Subscription(callback, func, inst, priority, filter_fn)
            self._subs.append(sub)
            self._subs.sort(key=lambda x: x.priority, reverse=True)
            return sub

    def unsubscribe(self, token_or_callback):
        with self._lock:
            if isinstance(token_or_callback, _Subscription):
                try:
                    self._subs.remove(token_or_callback)
                    return True
                except ValueError:
                    return False
            for s in list(self._subs):
                if s.matches(token_or_callback):
                    self._subs.remove(s)
                    return True
            return False

    def notify_all(self, message: Any):
        self.last_message = message
        with self._lock:
            subscribers = list(self._subs)
        for s in subscribers:
            if s.filter_fn and not s.filter_fn(message):
                continue
            try:
                s.callback(message)
            except Exception:
                continue

if __name__ == "__main__":
    class Logger:
        def __init__(self, name):
            self.name = name
        def handle(self, msg):
            print(f"{self.name} received: {msg}")

    notifier = Notifier()
    a = Logger("A")
    b = Logger("B")

    # subscribe bound methods with different priorities and a filter
    tok_a = notifier.subscribe(a.handle, priority=10)
    tok_b = notifier.subscribe(b.handle, priority=5, filter_fn=lambda m: "important" in str(m))

    notifier.notify_all("an important update")
    notifier.notify_all("a minor note")

    # unsubscribe by token and by callback
    notifier.unsubscribe(tok_b)
    notifier.notify_all("another important update")