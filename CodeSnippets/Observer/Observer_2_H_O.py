import threading
import weakref
import uuid
import sys

try:
    ExceptionGroupAvailable = sys.version_info >= (3, 11)
except Exception:
    ExceptionGroupAvailable = False

class SubscriptionToken:
    def __init__(self):
        self._id = uuid.uuid4()
    @property
    def id(self):
        return self._id
    def __repr__(self):
        return f"<SubscriptionToken {self._id}>"

class SubscriberEntry:
    def __init__(self, callback, priority=0, use_weak=True):
        self.priority = priority
        self._strong = None
        self._ref = None
        self._alive = True
        self._id = uuid.uuid4()
        if use_weak:
            self._assign_weak(callback)
        else:
            self._strong = callback

    def _assign_weak(self, callback):
        try:
            if hasattr(callback, "__self__") and hasattr(callback, "__func__"):
                self._ref = weakref.WeakMethod(callback)
            else:
                self._ref = weakref.ref(callback)
                if self._ref() is None:
                    raise TypeError
        except Exception:
            self._strong = callback
            self._ref = None

    def get_callable(self):
        if self._strong is not None:
            return self._strong
        if self._ref is None:
            return None
        fn = self._ref()
        if fn is None:
            self._alive = False
        return fn

    def alive(self):
        if not self._alive:
            return False
        if self._strong is not None:
            return True
        return self._ref() is not None

    def matches(self, token_or_cb):
        if isinstance(token_or_cb, SubscriptionToken):
            return getattr(token_or_cb, "id", None) == self._id
        cb = token_or_cb
        target = self.get_callable()
        return target is cb

    @property
    def identifier(self):
        return self._id

class Publisher:
    def __init__(self):
        self._lock = threading.RLock()
        self._entries = []
        self._token_map = {}
        self._paused = False

    def add_listener(self, callback, priority=0, weak=True):
        token = SubscriptionToken()
        entry = SubscriberEntry(callback, priority=priority, use_weak=weak)
        entry_id = entry.identifier
        with self._lock:
            self._entries.append(entry)
            self._entries.sort(key=lambda e: -e.priority)
            self._token_map[entry_id] = entry
        token._id = entry_id
        return token

    def remove_listener(self, token_or_callback):
        with self._lock:
            to_remove = []
            for e in list(self._entries):
                if e.matches(token_or_callback):
                    to_remove.append(e)
            for e in to_remove:
                self._entries.remove(e)
                self._token_map.pop(e.identifier, None)
            return len(to_remove)

    def pause(self):
        with self._lock:
            self._paused = True

    def resume(self):
        with self._lock:
            self._paused = False

    def notify(self, *args, **kwargs):
        with self._lock:
            if self._paused:
                return
            snapshot = list(self._entries)
        exceptions = []
        for entry in snapshot:
            cb = entry.get_callable()
            if cb is None:
                with self._lock:
                    if entry in self._entries:
                        self._entries.remove(entry)
                        self._token_map.pop(entry.identifier, None)
                continue
            try:
                cb(*args, **kwargs)
            except Exception as exc:
                exceptions.append(exc)
                with self._lock:
                    if entry in self._entries:
                        pass
        if exceptions:
            if ExceptionGroupAvailable:
                raise ExceptionGroup("Multiple listener errors", exceptions)
            else:
                msgs = "; ".join(f"{type(e).__name__}: {e}" for e in exceptions)
                raise RuntimeError(f"Multiple listener errors: {msgs}")

if __name__ == "__main__":
    pub = Publisher()

    def free_handler(msg):
        print("free_handler received:", msg)

    token_free = pub.add_listener(free_handler, priority=1, weak=False)

    class Handler:
        def __init__(self, name):
            self.name = name
            self._token = None

        def register(self, publisher, priority=0, weak=True):
            self._token = publisher.add_listener(self.method, priority=priority, weak=weak)

        def method(self, msg):
            print(f"{self.name} got: {msg}")
            if "remove-me" in msg and self._token:
                pub.remove_listener(self._token)

        def raising(self, msg):
            raise ValueError(f"{self.name} failed on {msg}")

    h1 = Handler("A")
    h2 = Handler("B")
    h1.register(pub, priority=2)
    h2.register(pub, priority=0)

    token_raising = pub.add_listener(h2.raising, priority=3, weak=True)

    print("First notify:")
    try:
        pub.notify("hello")
    except Exception as e:
        print("Exception during notify:", e)

    print("\nNotify that causes removal during callback:")
    pub.notify("please remove-me now")

    print("\nDelete h1 and run GC to demonstrate weak cleanup:")
    del h1
    import gc
    gc.collect()
    pub.notify("after gc")

    print("\nRemove free handler and notify:")
    pub.remove_listener(token_free)
    try:
        pub.notify("final")
    except Exception as e:
        print("Exception during final notify:", e)