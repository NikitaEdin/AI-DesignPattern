import weakref
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class SubscriberHandle:
    def __init__(self, sid, broker):
        self._id = sid
        self._broker = broker
    def detach(self):
        self._broker.unsubscribe(self)
    def __eq__(self, other):
        return isinstance(other, SubscriberHandle) and self._id == other._id
    def __hash__(self):
        return hash(self._id)

class _Entry:
    def __init__(self, sid, callback, predicate, priority, weak):
        self.id = sid
        self.predicate = predicate
        self.priority = priority
        self._strong = None
        self._ref = None
        if weak:
            if hasattr(callback, "__self__") and hasattr(callback, "__func__"):
                try:
                    self._ref = weakref.WeakMethod(callback)
                except TypeError:
                    self._strong = callback
            else:
                try:
                    self._ref = weakref.ref(callback)
                except TypeError:
                    self._strong = callback
        else:
            self._strong = callback
    def alive(self):
        if self._strong is not None:
            return True
        return self._ref() is not None
    def get(self):
        if self._strong is not None:
            return self._strong
        return self._ref()

class Publisher:
    def __init__(self, max_workers=4):
        self._lock = threading.RLock()
        self._subs = []
        self._counter = 0
        self._executor = ThreadPoolExecutor(max_workers=max_workers) if max_workers and max_workers > 0 else None
    def subscribe(self, callback, predicate=None, priority=0, weak=True):
        with self._lock:
            self._counter += 1
            sid = self._counter
            entry = _Entry(sid, callback, predicate, priority, weak)
            self._subs.append(entry)
            return SubscriberHandle(sid, self)
    def unsubscribe(self, handle):
        with self._lock:
            self._subs = [s for s in self._subs if s.id != handle._id]
    def _cleanup_locked(self):
        self._subs = [s for s in self._subs if s.alive()]
    def publish(self, *args, swallow_exceptions=True, async_mode=False, **kwargs):
        with self._lock:
            self._cleanup_locked()
            entries = [s for s in self._subs]
        entries.sort(key=lambda e: e.priority, reverse=True)
        targets = []
        for e in entries:
            cb = e.get()
            if cb is None:
                continue
            if e.predicate and not e.predicate(*args, **kwargs):
                continue
            targets.append((e, cb))
        errors = []
        if async_mode and self._executor:
            future_map = {}
            for e, cb in targets:
                def _run(func, ent, a, kw):
                    try:
                        return func(*a, **kw)
                    except Exception as exc:
                        return exc
                fut = self._executor.submit(_run, cb, e, args, kwargs)
                future_map[fut] = (e, cb)
            for fut in as_completed(future_map):
                ent, cb = future_map[fut]
                res = fut.result()
                if isinstance(res, Exception):
                    if swallow_exceptions:
                        errors.append((SubscriberHandle(ent.id, self), res))
                    else:
                        raise res
        else:
            for e, cb in targets:
                try:
                    cb(*args, **kwargs)
                except Exception as exc:
                    if swallow_exceptions:
                        errors.append((SubscriberHandle(e.id, self), exc))
                    else:
                        raise
        return errors

if __name__ == "__main__":
    pub = Publisher(max_workers=3)
    def global_listener(msg):
        print("global:", msg)
    handle_global = pub.subscribe(global_listener, priority=1)
    handle_filtered = pub.subscribe(lambda m: print("filtered:", m), predicate=lambda m: "ok" in m)
    class Receiver:
        def __init__(self, name):
            self.name = name
        def notify(self, message):
            print(self.name, "received", message)
    r = Receiver("A")
    handle_method = pub.subscribe(r.notify, priority=2, weak=True)
    print("Synchronous dispatch:")
    pub.publish("test ok", async_mode=False)
    print("Asynchronous dispatch:")
    pub.publish("async ok", async_mode=True)
    print("Unsubscribe global and delete receiver:")
    handle_global.detach()
    del r
    pub.publish("after delete ok", async_mode=False)
    print("Exception handling (swallowed):")
    def bad(msg):
        raise ValueError("boom")
    pub.subscribe(bad)
    errs = pub.publish("will boom", swallow_exceptions=True)
    print("Captured errors:", [(h._id, type(e).__name__) for h,e in errs])
    print("Done.")