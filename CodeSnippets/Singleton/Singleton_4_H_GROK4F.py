import threading
import pickle
import copy

class CentralLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(CentralLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logs = []
            self.timestamp = threading.current_thread().name

    def record_entry(self, message):
        self.logs.append(f"[{self.timestamp}] {message}")

    def retrieve_entries(self):
        return self.logs.copy()

    def clear_entries(self):
        self.logs.clear()

    def __reduce__(self):
        return (self.__class__, ())

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

if __name__ == "__main__":
    first_ref = CentralLogger()
    second_ref = CentralLogger()
    print(first_ref is second_ref)
    first_ref.record_entry("Initial message")

    def thread_task(ident):
        logger = CentralLogger()
        logger.record_entry(f"Message from thread {ident}")
        entries = logger.retrieve_entries()
        print(f"Thread {ident} sees {len(entries)} entries")

    threads = []
    for i in range(5):
        t = threading.Thread(target=thread_task, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    all_entries = first_ref.retrieve_entries()
    print(f"Total entries after threads: {len(all_entries)}")
    print("Sample entries:", all_entries[-3:])

    first_ref.clear_entries()

    serialized = pickle.dumps(first_ref)
    deserialized = pickle.loads(serialized)
    print("Deserialized is same instance:", deserialized is first_ref)

    copied = copy.copy(first_ref)
    print("Copied is same instance:", copied is first_ref)

    deep_copied = copy.deepcopy(first_ref)
    print("Deep copied is same instance:", deep_copied is first_ref)