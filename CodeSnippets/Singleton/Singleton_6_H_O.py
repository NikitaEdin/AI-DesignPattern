import threading
import copy
import pickle

class InstanceRegistryMeta(type):
    _instances = {}
    _locks = {}
    _under_construction = {}
    _global_lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        meta = type(cls)

        # Fast path: already initialized
        inst = meta._instances.get(cls)
        if inst is not None:
            return inst

        # Ensure a per-class lock exists (create under global lock)
        with meta._global_lock:
            lock = meta._locks.get(cls)
            if lock is None:
                lock = threading.RLock()
                meta._locks[cls] = lock

        # Acquire per-class lock to serialize creation
        with lock:
            # Re-check in case another thread completed creation
            inst = meta._instances.get(cls)
            if inst is not None:
                return inst

            # Re-entrant construction detection (same thread recursive call)
            in_prog = meta._under_construction.get(cls)
            if in_prog is not None:
                return in_prog

            # Allocate instance without publishing it until init finishes
            inst = object.__new__(cls)
            meta._under_construction[cls] = inst
            try:
                cls.__init__(inst, *args, **kwargs)
            except Exception:
                # Clean up on failure
                meta._under_construction.pop(cls, None)
                raise
            # Initialization complete: publish instance and remove placeholder
            meta._instances[cls] = inst
            meta._under_construction.pop(cls, None)
            # Mark initialized for cooperative subclasses
            try:
                setattr(inst, "_initialized", True)
            except Exception:
                pass
            return inst

    def reset_instance(cls):
        meta = type(cls)
        with meta._global_lock:
            lock = meta._locks.get(cls)
            if lock is not None:
                # Acquire per-class lock to ensure no concurrent construction
                with lock:
                    inst = meta._instances.pop(cls, None)
                    # Optional cleanup hook
                    if inst is not None:
                        for name in ("close", "dispose", "shutdown"):
                            fn = getattr(inst, name, None)
                            if callable(fn):
                                try:
                                    fn()
                                except Exception:
                                    pass
                    # Remove lock entry so next creation will reconstruct it
                    meta._locks.pop(cls, None)
            else:
                # No lock exists; just remove instance if present
                meta._instances.pop(cls, None)

class InstanceEnforced(metaclass=InstanceRegistryMeta):
    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __reduce__(self):
        # Unpickling will call the class, which returns the registered instance.
        return (self.__class__, ())

# Example usage
class ConfigManager(InstanceEnforced):
    def __init__(self, source=None):
        # Cooperative guard to avoid reinitialization in recursive scenarios
        if getattr(self, "_initialized", False):
            return
        # Simulate initialization work
        self.source = source or "default"
        self.data = {"loaded_from": self.source}

    def get(self, key, default=None):
        return self.data.get(key, default)

def worker_thread(results, idx, source=None):
    obj = ConfigManager(source)
    results[idx] = id(obj)

if __name__ == "__main__":
    # Demonstrate same-instance across threads
    threads = []
    results = [None] * 4
    for i in range(4):
        t = threading.Thread(target=worker_thread, args=(results, i, "env"))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print("Instance ids from threads:", results)
    print("All equal:", all(x == results[0] for x in results))

    # Show reset behavior
    a = ConfigManager("first")
    print("Before reset:", id(a), a.source)
    ConfigManager.reset_instance()
    b = ConfigManager("second")
    print("After reset:", id(b), b.source)

    # Copy and pickle behavior
    c = ConfigManager()
    cp = copy.copy(c)
    xp = pickle.loads(pickle.dumps(c))
    print("copy is same:", cp is c)
    print("pickle restored is same:", xp is c)