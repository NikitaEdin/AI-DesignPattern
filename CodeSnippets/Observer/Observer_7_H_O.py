import threading
import weakref
import types
import itertools
import traceback

class SubscriptionToken:
    def __init__(self, publisher_ref, token_id):
        self._publisher_ref = publisher_ref
        self._id = token_id

    def cancel(self):
        publisher = self._publisher_ref()
        if publisher:
            publisher.unregister(token=self)

class Publisher:
    def __init__(self):
        self._lock = threading.RLock()
        self._entries = {}
        self._counter = itertools.count()
    
    def _make_weak(self, callback):
        if isinstance(callback, types.MethodType):
            return weakref.WeakMethod(callback)
        try:
            return weakref.ref(callback)
        except TypeError:
            raise TypeError("Callback is not weak-referenceable")
    
    def register(self, callback, filter_fn=None, one_shot=False, priority=0):
        ref = self._make_weak(callback)
        token_id = next(self._counter)
        entry = {"ref": ref, "filter": filter_fn, "one_shot": one_shot, "priority": priority}
        with self._lock:
            self._entries[token_id] = entry
        return SubscriptionToken(weakref.ref(self), token_id)
    
    def unregister(self, callback=None, token=None):
        with self._lock:
            if token is not None:
                tid = token._id
                self._entries.pop(tid, None)
                return
            if callback is not None:
                to_remove = []
                for tid, entry in self._entries.items():
                    cb = entry["ref"]()
                    if cb is None:
                        to_remove.append(tid)
                        continue
                    if cb == callback:
                        to_remove.append(tid)
                for tid in to_remove:
                    self._entries.pop(tid, None)
    
    def notify(self, event=None, **kwargs):
        exceptions = []
        to_remove = []
        with self._lock:
            items = list(self._entries.items())
        items.sort(key=lambda it: it[1]["priority"], reverse=True)
        for tid, entry in items:
            cb_ref = entry["ref"]
            callback = cb_ref()
            if callback is None:
                with self._lock:
                    self._entries.pop(tid, None)
                continue
            try:
                filt = entry["filter"]
                if filt is not None and not filt(event, **kwargs):
                    continue
                callback(event, **kwargs)
            except Exception:
                exceptions.append((tid, traceback.format_exc()))
            else:
                if entry["one_shot"]:
                    to_remove.append(tid)
        if to_remove:
            with self._lock:
                for tid in to_remove:
                    self._entries.pop(tid, None)
        return exceptions

if __name__ == "__main__":
    pub = Publisher()

    class Worker:
        def __init__(self, name):
            self.name = name
        def handle(self, event, **data):
            print(f"{self.name} received {event} with {data}")
            if data.get("cause") == "error" and self.name == "w2":
                raise RuntimeError("simulated")

    w1 = Worker("w1")
    w2 = Worker("w2")

    def free_handler(event, **data):
        print("free_handler got", event, data)

    token1 = pub.register(w1.handle, priority=10)
    token2 = pub.register(w2.handle, priority=5)
    token3 = pub.register(free_handler, filter_fn=lambda e, **d: e == "update")
    oneshot = pub.register(lambda e, **d: print("one-shot got", e), one_shot=True)

    print("First notify:")
    errors = pub.notify("update", payload=123)
    for tid, exc in errors:
        print("Error in handler", tid, exc)

    print("Second notify with error trigger:")
    errors = pub.notify("update", payload=456, cause="error")
    for tid, exc in errors:
        print("Error in handler", tid, exc)

    print("Unregistering w1")
    token1.cancel()

    print("Final notify:")
    pub.notify("final", info="done")