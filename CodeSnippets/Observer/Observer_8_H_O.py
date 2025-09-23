import threading
import weakref
import itertools
from typing import Callable, Optional, Any, Iterable, List, Tuple


class Subscription:
    def __init__(self, callback: Callable, filter_fn: Optional[Callable[[Tuple, dict], bool]], priority: int, once: bool, weak: bool, seq: int):
        self._seq = seq
        self.filter_fn = filter_fn
        self.priority = priority
        self.once = once
        self._strong = False
        try:
            if weak:
                if hasattr(callback, "__self__") and hasattr(callback, "__func__"):
                    self._ref = weakref.WeakMethod(callback)
                else:
                    self._ref = weakref.ref(callback)
            else:
                raise TypeError
        except TypeError:
            self._ref = callback
            self._strong = True

    def callback(self) -> Optional[Callable]:
        if self._strong:
            return self._ref
        try:
            cb = self._ref()
            return cb
        except Exception:
            return None

    def alive(self) -> bool:
        return self.callback() is not None

    def matches(self, other: Any) -> bool:
        cb = self.callback()
        if cb is None:
            return False
        return cb is other or self is other

    def deliver(self, *args, **kwargs) -> Optional[Exception]:
        cb = self.callback()
        if cb is None:
            return None
        try:
            if self.filter_fn:
                ok = self.filter_fn(args, kwargs)
                if not ok:
                    return None
            cb(*args, **kwargs)
        except Exception as exc:
            return exc
        return None


class Publisher:
    def __init__(self):
        self._lock = threading.RLock()
        self._subs: List[Subscription] = []
        self._counter = itertools.count()

    def subscribe(self, callback: Callable, *, filter_fn: Optional[Callable[[Tuple, dict], bool]] = None, priority: int = 0, once: bool = False, weak: bool = True) -> Subscription:
        with self._lock:
            seq = next(self._counter)
            sub = Subscription(callback, filter_fn, priority, once, weak, seq)
            self._subs.append(sub)
            self._subs.sort(key=lambda s: (-s.priority, s._seq))
            return sub

    def unsubscribe(self, token_or_callback: Any) -> bool:
        with self._lock:
            for i, s in enumerate(list(self._subs)):
                if s.matches(token_or_callback):
                    del self._subs[i]
                    return True
            return False

    def notify(self, *args, **kwargs) -> List[Exception]:
        errors: List[Exception] = []
        to_remove: List[Subscription] = []
        with self._lock:
            subs_snapshot = list(self._subs)
        for s in subs_snapshot:
            if not s.alive():
                to_remove.append(s)
                continue
            err = s.deliver(*args, **kwargs)
            if err:
                errors.append(err)
            if s.once:
                to_remove.append(s)
        if to_remove:
            with self._lock:
                for r in to_remove:
                    try:
                        self._subs.remove(r)
                    except ValueError:
                        pass
        return errors

    def clear(self):
        with self._lock:
            self._subs.clear()

    def count(self) -> int:
        with self._lock:
            return len(self._subs)


if __name__ == "__main__":
    pub = Publisher()

    def logger(msg, **kw):
        print("logger received:", msg, kw)

    def errorer(msg, **kw):
        if "bad" in msg:
            raise RuntimeError("bad message")
        print("errorer ok:", msg)

    class Handler:
        def method(self, msg, **kw):
            print("method got:", msg)

    h = Handler()

    pub.subscribe(logger, priority=1)
    pub.subscribe(errorer, priority=0)
    token = pub.subscribe(h.method, priority=2, weak=True)
    pub.subscribe(lambda args, kwargs: None, filter_fn=lambda a, k: False)
    pub.subscribe(lambda msg, **kw: print("one-shot:", msg), once=True)

    print("First notify")
    errors = pub.notify("hello", extra=1)
    for e in errors:
        print("Error:", e)

    print("Second notify with bad")
    errors = pub.notify("this is bad", extra=2)
    for e in errors:
        print("Error:", e)

    print("Unsubscribe method")
    pub.unsubscribe(token)
    pub.notify("after unsubscribe")

    print("Count:", pub.count())

    def make_temporary():
        class Temp:
            def cb(self, msg, **kw):
                print("temp cb:", msg)
        t = Temp()
        pub.subscribe(t.cb, weak=True)
    make_temporary()
    import gc
    gc.collect()
    print("After GC notify")
    pub.notify("post-gc")