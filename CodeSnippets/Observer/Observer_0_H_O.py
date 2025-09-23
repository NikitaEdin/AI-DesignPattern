import threading
import weakref
import types
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Optional, Set

@dataclass
class Subscription:
    priority: int
    seq: int
    once: bool
    event_types: Optional[Set[Any]]
    inst_ref: Optional[weakref.ref] = None
    func: Optional[Callable] = None
    func_ref: Optional[weakref.ref] = None

    def resolve(self) -> Optional[Callable]:
        if self.inst_ref is not None and self.func is None:
            inst = self.inst_ref()
            if inst is None:
                return None
            return getattr(inst, "__call__", None)
        if self.inst_ref is not None and self.func is not None:
            inst = self.inst_ref()
            if inst is None:
                return None
            return types.MethodType(self.func, inst)
        if self.func is not None and self.func_ref is not None:
            f = self.func_ref()
            return f
        if self.func is not None and self.func_ref is None:
            return self.func
        return None

class Notifier:
    def __init__(self):
        self._lock = threading.RLock()
        self._subs: list[Subscription] = []
        self._seq = 0

    def _decompose(self, callback: Callable) -> Subscription:
        if callback is None or not callable(callback):
            raise TypeError("callback must be callable")
        # bound method
        if isinstance(callback, types.MethodType) and callback.__self__ is not None:
            inst = callback.__self__
            func = callback.__func__
            try:
                inst_ref = weakref.ref(inst)
            except TypeError:
                inst_ref = None
            try:
                func_ref = weakref.ref(func)
            except TypeError:
                func_ref = None
            sub = Subscription(0, 0, False, None, inst_ref, func, func_ref)
            return sub
        # function
        if isinstance(callback, types.FunctionType):
            try:
                func_ref = weakref.ref(callback)
                sub = Subscription(0, 0, False, None, None, callback, func_ref)
            except TypeError:
                sub = Subscription(0, 0, False, None, None, callback, None)
            return sub
        # callable object instance
        # store weakref to instance and mark func as None so resolve uses __call__
        try:
            inst_ref = weakref.ref(callback)
            return Subscription(0, 0, False, None, inst_ref, None, None)
        except TypeError:
            # fallback: keep strong reference to callable
            return Subscription(0, 0, False, None, None, callback, None)

    def subscribe(self, callback: Callable, *, priority: int = 0, once: bool = False,
                  event_types: Optional[Iterable[Any]] = None) -> int:
        if event_types is not None:
            typeset = frozenset(event_types)
            if len(typeset) == 0:
                raise ValueError("event_types must be None or non-empty iterable")
        else:
            typeset = None
        sub = self._decompose(callback)
        with self._lock:
            self._seq += 1
            sub.priority = priority
            sub.seq = self._seq
            sub.once = bool(once)
            sub.event_types = typeset
            self._subs.append(sub)
            self._subs.sort(key=lambda s: (-s.priority, s.seq))
            return sub.seq

    def unsubscribe(self, callback: Optional[Callable] = None, token: Optional[int] = None) -> bool:
        if callback is None and token is None:
            raise ValueError("provide callback or token to unsubscribe")
        with self._lock:
            if token is not None:
                for i, s in enumerate(self._subs):
                    if s.seq == token:
                        del self._subs[i]
                        return True
                return False
            # match by callback: decompose and compare
            target = self._decompose(callback)
            for i, s in enumerate(self._subs):
                if s.func is not None and target.func is not None:
                    # both have func; compare by function object identity
                    if s.func is target.func:
                        # if bound method compare instance identity
                        if s.inst_ref is None and target.inst_ref is None:
                            del self._subs[i]
                            return True
                        si = s.inst_ref() if s.inst_ref else None
                        ti = target.inst_ref() if target.inst_ref else None
                        if si is ti:
                            del self._subs[i]
                            return True
                elif s.inst_ref is not None and target.inst_ref is not None and s.func is None and target.func is None:
                    # callable-instance case
                    if s.inst_ref() is target.inst_ref():
                        del self._subs[i]
                        return True
            return False

    def notify(self, event_type: Any = None, *args, **kwargs) -> list[Exception]:
        with self._lock:
            subs_snapshot = list(self._subs)
        to_remove_seqs: set[int] = set()
        errors: list[Exception] = []
        for s in subs_snapshot:
            if s.event_types is not None and event_type not in s.event_types:
                continue
            cb = s.resolve()
            if cb is None:
                to_remove_seqs.add(s.seq)
                continue
            try:
                cb(event_type, *args, **kwargs)
            except Exception as exc:
                errors.append(exc)
            if s.once:
                to_remove_seqs.add(s.seq)
        if to_remove_seqs:
            with self._lock:
                self._subs = [s for s in self._subs if s.seq not in to_remove_seqs and s.resolve() is not None]
        return errors

if __name__ == "__main__":
    notifier = Notifier()

    def free_fn(evt, msg):
        print("free_fn got", evt, msg)

    class Handler:
        def __init__(self, name):
            self.name = name
        def on_event(self, evt, msg):
            print(self.name, "received", evt, msg)
        def __call__(self, evt, msg):
            print(self.name, "__call__", evt, msg)

    h1 = Handler("A")
    h2 = Handler("B")

    # subscribe various callables
    t1 = notifier.subscribe(free_fn, priority=5)
    t2 = notifier.subscribe(h1.on_event, priority=10, once=True)
    t3 = notifier.subscribe(h2, priority=1)  # callable object -> __call__
    t4 = notifier.subscribe(lambda evt, msg: print("lambda got", evt, msg), event_types=["alpha"])

    print("First notify alpha:")
    notifier.notify("alpha", "hello")

    print("Second notify beta:")
    notifier.notify("beta", "world")

    print("Unsubscribe free_fn by callback:")
    notifier.unsubscribe(free_fn)

    print("Third notify alpha after unreg:")
    notifier.notify("alpha", "again")