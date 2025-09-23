import threading
import weakref
import logging
from typing import Any, Callable, Optional, List, Tuple

class Notifier:
    def __init__(self):
        self._lock = threading.RLock()
        self._entries: List[dict] = []
        self._counter = 0

    def _callable_id(self, fn: Callable) -> Tuple:
        if hasattr(fn, "__self__") and hasattr(fn, "__func__"):
            return ("bound", id(fn.__self__), id(fn.__func__))
        if hasattr(fn, "__call__") and not hasattr(fn, "__func__"):
            return ("callable_obj", id(fn))
        return ("func", id(fn))

    def register(self, handler: Callable, *, priority: int = 0, predicate: Optional[Callable[[Any], bool]] = None, strong: bool = False) -> None:
        with self._lock:
            try:
                if not strong:
                    if hasattr(handler, "__self__") and hasattr(handler, "__func__"):
                        ref = weakref.WeakMethod(handler)
                        is_weak = True
                    else:
                        ref = weakref.ref(handler)
                        is_weak = True
                else:
                    raise TypeError
            except Exception:
                ref = handler
                is_weak = False
            entry = {
                "priority": priority,
                "key": (self._counter, self._callable_id(handler)),
                "ref": ref,
                "is_weak": is_weak,
                "predicate": predicate,
            }
            self._counter += 1
            self._entries.append(entry)
            self._entries.sort(key=lambda e: (-e["priority"], e["key"][0]))

    def remove(self, handler: Callable) -> bool:
        target_id = self._callable_id(handler)
        removed = False
        with self._lock:
            new_entries = []
            for e in self._entries:
                if e["key"][1] == target_id:
                    removed = True
                    continue
                new_entries.append(e)
            self._entries = new_entries
        return removed

    def _resolve(self, entry: dict) -> Optional[Callable]:
        if entry["is_weak"]:
            try:
                return entry["ref"]()
            except Exception:
                return None
        return entry["ref"]

    def dispatch(self, event: Any, **kwargs) -> List[Tuple[Callable, Optional[Exception]]]:
        results: List[Tuple[Callable, Optional[Exception]]] = []
        with self._lock:
            entries_snapshot = list(self._entries)
        for entry in entries_snapshot:
            fn = self._resolve(entry)
            if fn is None:
                with self._lock:
                    if entry in self._entries:
                        try:
                            self._entries.remove(entry)
                        except ValueError:
                            pass
                continue
            pred = entry.get("predicate")
            try:
                if pred is None or pred(event, **kwargs):
                    try:
                        fn(event, **kwargs)
                        results.append((fn, None))
                    except Exception as exc:
                        logging.exception("Handler raised during dispatch")
                        results.append((fn, exc))
            except Exception as exc:
                logging.exception("Predicate raised during dispatch")
                results.append((fn, exc))
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    notifier = Notifier()

    def free_function(event, **kwargs):
        print("free_function received:", event, kwargs)

    class Receiver:
        def __init__(self, name):
            self.name = name
        def handle(self, event, **kwargs):
            print(f"{self.name} got:", event, kwargs)
            if kwargs.get("fail"):
                raise RuntimeError("simulated")

    r1 = Receiver("A")
    r2 = Receiver("B")

    notifier.register(free_function, priority=5)
    notifier.register(r1.handle, priority=10)
    notifier.register(r2.handle, priority=1, predicate=lambda e, **k: e != "ignore")

    print("First dispatch:")
    notifier.dispatch("hello", extra=123)

    print("\nDispatch with failure:")
    notifier.dispatch("test", fail=True)

    print("\nRemove r1 and dispatch:")
    notifier.remove(r1.handle)
    notifier.dispatch("after_remove")

    print("\nDispatch ignored by predicate:")
    notifier.dispatch("ignore")