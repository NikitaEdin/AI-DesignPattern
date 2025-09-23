import weakref
import threading
import traceback

class Subscription:
    def __init__(self, callback, event_type=None, once=False, priority=0):
        self._is_method = hasattr(callback, "__self__") and callback.__self__ is not None
        self._ref = weakref.WeakMethod(callback) if self._is_method else weakref.ref(callback)
        self.event_type = event_type
        self.once = once
        self.priority = priority
        self._alive = True

    def is_alive(self):
        if not self._alive:
            return False
        return self._ref() is not None

    def matches(self, event_type):
        return self.event_type is None or self.event_type == event_type

    def notify(self, event_type, payload):
        fn = self._ref()
        if fn is None:
            self._alive = False
            return False
        try:
            fn(event_type, payload)
        except Exception:
            traceback.print_exc()
        return True

    def cancel(self):
        self._alive = False

class Publisher:
    def __init__(self):
        self._lock = threading.RLock()
        self._subs = []
        self._last_events = {}

    def subscribe(self, callback, event_type=None, once=False, priority=0, replay_last=False):
        sub = Subscription(callback, event_type=event_type, once=once, priority=priority)
        with self._lock:
            self._subs.append(sub)
            self._subs.sort(key=lambda s: s.priority, reverse=True)
            if replay_last and (event_type in self._last_events or None in self._last_events):
                key = event_type if event_type in self._last_events else None
                event = self._last_events.get(key)
                if event is not None:
                    sub.notify(event[0], event[1])
                    if sub.once:
                        sub.cancel()
        return sub

    def unsubscribe(self, token_or_callback):
        with self._lock:
            if isinstance(token_or_callback, Subscription):
                token_or_callback.cancel()
                self._subs = [s for s in self._subs if s.is_alive()]
                return True
            target = token_or_callback
            removed = False
            for s in list(self._subs):
                fn = s._ref()
                if fn is None:
                    s.cancel()
                    continue
                if fn == target or getattr(fn, "__func__", None) == getattr(target, "__func__", None):
                    s.cancel()
                    removed = True
            self._subs = [s for s in self._subs if s.is_alive()]
            return removed

    def publish(self, event_type, payload=None, store_last=True):
        with self._lock:
            if store_last:
                self._last_events[event_type] = (event_type, payload)
            subs_snapshot = list(self._subs)
        to_remove = []
        for s in subs_snapshot:
            if not s.is_alive():
                to_remove.append(s)
                continue
            if not s.matches(event_type):
                continue
            ok = s.notify(event_type, payload)
            if not ok or s.once:
                s.cancel()
                to_remove.append(s)
        if to_remove:
            with self._lock:
                self._subs = [s for s in self._subs if s.is_alive()]

if __name__ == "__main__":
    pub = Publisher()

    def logger(ev, data):
        print(f"logger received {ev}: {data}")

    class Handler:
        def __init__(self, name):
            self.name = name
        def on_event(self, ev, data):
            print(f"{self.name} got {ev} -> {data}")
            if ev == "stop":
                raise RuntimeError("example error")

    h1 = Handler("H1")
    h2 = Handler("H2")

    s1 = pub.subscribe(logger, priority=1)
    s2 = pub.subscribe(h1.on_event, event_type="update", priority=5)
    s3 = pub.subscribe(h2.on_event, once=True, replay_last=True)
    pub.publish("update", {"value": 42})
    pub.publish("update", {"value": 43})
    pub.publish("stop", None)
    pub.unsubscribe(s1)
    pub.publish("update", {"value": 44})
    def late(ev, data):
        print("late subscriber got", ev, data)
    pub.subscribe(late, replay_last=True)