import threading
import weakref
import uuid
import inspect
import sys

class SubscriptionToken:
    def __init__(self, id):
        self.id = id
    def __repr__(self):
        return f"<Token {self.id}>"

class Subscription:
    def __init__(self, handler, event_filter=None, one_shot=False, priority=0):
        if not callable(handler):
            raise TypeError("handler must be callable")
        self.one_shot = bool(one_shot)
        self.priority = int(priority)
        self.filter = event_filter if event_filter is None or callable(event_filter) else None
        self.id = str(uuid.uuid4())
        if inspect.ismethod(handler):
            self._ref = weakref.WeakMethod(handler)
            self._is_method = True
        else:
            try:
                self._ref = weakref.ref(handler)
                self._is_method = False
            except TypeError:
                bound = getattr(handler, "__call__", None)
                if bound and inspect.ismethod(bound):
                    self._ref = weakref.WeakMethod(bound)
                    self._is_method = True
                else:
                    raise TypeError("handler is not weak-referenceable")

    def is_alive(self):
        return self._ref() is not None

    def matches(self, token):
        return self.id == getattr(token, "id", token)

    def call(self, event):
        target = self._ref()
        if target is None:
            return False
        try:
            if self.filter and not self.filter(event):
                return True
            if self._is_method:
                target(event)
            else:
                target(event)
            return True
        except Exception:
            return True

class Publisher:
    def __init__(self):
        self._lock = threading.RLock()
        self._subs = []

    def register(self, handler, event_filter=None, one_shot=False, priority=0):
        sub = Subscription(handler, event_filter=event_filter, one_shot=one_shot, priority=priority)
        token = SubscriptionToken(sub.id)
        with self._lock:
            self._subs.append(sub)
            self._subs.sort(key=lambda s: s.priority, reverse=True)
        return token

    def unregister(self, token):
        tid = getattr(token, "id", token)
        with self._lock:
            before = len(self._subs)
            self._subs = [s for s in self._subs if not s.matches(tid)]
            return before - len(self._subs)

    def notify(self, event):
        to_remove = []
        with self._lock:
            subs_snapshot = list(self._subs)
        for sub in subs_snapshot:
            alive = sub.is_alive()
            if not alive:
                to_remove.append(sub)
                continue
            proceed = sub.call(event)
            if not proceed:
                to_remove.append(sub)
                continue
            if sub.one_shot:
                to_remove.append(sub)
        if to_remove:
            with self._lock:
                current_ids = {s.id for s in self._subs}
                for r in to_remove:
                    if r.id in current_ids:
                        self._subs = [s for s in self._subs if s.id != r.id]

if __name__ == "__main__":
    pub = Publisher()

    class Logger:
        def __init__(self, name):
            self.name = name
        def handle(self, event):
            print(f"{self.name} received: {event}")

    logger_a = Logger("A")
    logger_b = Logger("B")

    token_a = pub.register(logger_a.handle, priority=10)
    token_b = pub.register(logger_b.handle, event_filter=lambda e: isinstance(e, dict), priority=5)
    token_c = pub.register(lambda e: print("one-shot lambda got:", e), one_shot=True, priority=20)

    pub.notify("simple event")
    pub.notify({"type": "dict", "payload": 123})
    pub.unregister(token_a)
    pub.notify("after unregister")