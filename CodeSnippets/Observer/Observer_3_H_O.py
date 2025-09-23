import threading, weakref, inspect, uuid, logging, time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, TimeoutError

logging.basicConfig(level=logging.INFO)

@dataclass
class Subscription:
    id: str
    key: tuple
    callback: object
    once: bool
    predicate: object
    priority: int

class Broadcaster:
    def __init__(self, async_workers: int | None = None):
        self._lock = threading.RLock()
        self._subs: list[Subscription] = []
        self._executor = ThreadPoolExecutor(max_workers=async_workers) if async_workers else None

    def _make_key(self, cb):
        if inspect.ismethod(cb):
            func = cb.__func__
            owner = cb.__self__
            try:
                owner_ref = weakref.ref(owner)
                return ("bound_weak", func, owner_ref)
            except TypeError:
                return ("bound_strong", func, owner)
        if inspect.isfunction(cb) or inspect.isbuiltin(cb):
            return ("func", cb)
        if callable(cb):
            return ("callable_obj", cb)
        return ("unknown", cb)

    def subscribe(self, callback, *, once=False, predicate=None, priority=0):
        key = self._make_key(callback)
        sub = Subscription(id=uuid.uuid4().hex, key=key, callback=callback, once=bool(once), predicate=predicate, priority=int(priority))
        with self._lock:
            self._subs.append(sub)
            self._subs.sort(key=lambda s: -s.priority)
        return sub.id

    def unsubscribe(self, *, callback=None, token=None):
        if callback is None and token is None:
            return 0
        key = self._make_key(callback) if callback is not None else None
        removed = 0
        with self._lock:
            new = []
            for s in self._subs:
                if token is not None and s.id == token:
                    removed += 1
                    continue
                if key is not None and self._keys_equal(s.key, key):
                    removed += 1
                    continue
                new.append(s)
            self._subs = new
        return removed

    def _keys_equal(self, a, b):
        if a[0].startswith("bound") and b[0].startswith("bound"):
            func_a, owner_a = a[1], a[2]
            func_b, owner_b = b[1], b[2]
            if func_a is not func_b:
                return False
            def owner_obj(x):
                if isinstance(x, weakref.ReferenceType):
                    return x()
                return x
            return owner_obj(owner_a) is owner_obj(owner_b)
        return a[0] == b[0] and a[1] is b[1]

    def publish(self, *args, asynchronous=False, timeout=None, **kwargs):
        with self._lock:
            subs = list(self._subs)
        to_call = []
        for s in subs:
            if s.key[0].startswith("bound") and s.key[2] if len(s.key) > 2 else True:
                if s.key[0] == "bound_weak" and isinstance(s.key[2], weakref.ReferenceType) and s.key[2]() is None:
                    continue
            if s.predicate:
                try:
                    if not s.predicate(*args, **kwargs):
                        continue
                except Exception:
                    logging.exception("Predicate error")
                    continue
            to_call.append(s)
        invoked_ids = set()
        if asynchronous and self._executor:
            fut_map = {}
            for s in to_call:
                fut = self._executor.submit(self._safe_invoke, s, *args, **kwargs)
                fut_map[fut] = s
            try:
                done, not_done = wait(list(fut_map.keys()), timeout=timeout)
            except Exception:
                done = set()
                not_done = set(fut_map.keys())
            for f in done:
                s = fut_map.get(f)
                try:
                    f.result()
                    invoked_ids.add(s.id)
                except Exception:
                    logging.exception("Callback raised in async")
            if not_done:
                logging.warning("Some async handlers did not complete before timeout")
        else:
            for s in to_call:
                ok = self._safe_invoke(s, *args, **kwargs)
                if ok:
                    invoked_ids.add(s.id)
        with self._lock:
            new = []
            for s in self._subs:
                if s.key[0] == "bound_weak" and isinstance(s.key[2], weakref.ReferenceType) and s.key[2]() is None:
                    continue
                if s.once and s.id in invoked_ids:
                    continue
                new.append(s)
            self._subs = new

    def _safe_invoke(self, s, *args, **kwargs):
        try:
            if s.key[0].startswith("bound"):
                func = s.key[1]
                owner = s.key[2]
                if isinstance(owner, weakref.ReferenceType):
                    inst = owner()
                    if inst is None:
                        return False
                    func(inst, *args, **kwargs)
                else:
                    func(owner, *args, **kwargs)
            elif s.key[0] == "func":
                s.key[1](*args, **kwargs)
            else:
                s.callback(*args, **kwargs)
            return True
        except Exception:
            logging.exception("Handler error")
            return False

    def close(self):
        if self._executor:
            self._executor.shutdown(wait=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

if __name__ == "__main__":
    class Handler:
        def __init__(self, name):
            self.name = name
        def notify(self, msg):
            print(f"{self.name} received: {msg}")

    def free_func(msg):
        print("free_func got:", msg)

    class Functor:
        def __call__(self, msg):
            print("Functor:", msg)

    h = Handler("A")
    f = Functor()
    with Broadcaster(async_workers=2) as b:
        t1 = b.subscribe(h.notify, once=False, priority=10)
        t2 = b.subscribe(free_func, once=False)
        t3 = b.subscribe(f, once=True)
        b.publish("first sync")
        b.publish("second async", asynchronous=True, timeout=1)
        b.unsubscribe(callback=h.notify)
        b.publish("after unsubscribe")
        time.sleep(0.2)