import threading
import pickle

class InstanceEnforcer(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if args or kwargs:
            raise ValueError("Instance creation with parameters is not permitted.")
        with _lock:
            if cls not in _instances:
                _instances[cls] = super(InstanceEnforcer, cls).__call__()
            return _instances[cls]

class CentralLogger(metaclass=InstanceEnforcer):
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(f"{threading.current_thread().name}: {message}")

    def get_logs(self):
        return self.logs[:]

    def __reduce__(self):
        return (self.__class__, ())

class ErrorHandler(CentralLogger):
    def __init__(self):
        super().__init__()
        self.errors = []

    def report(self, error):
        self.errors.append(error)

if __name__ == "__main__":
    # Basic instance sharing
    logger1 = CentralLogger()
    logger1.log("Main message")
    logger2 = CentralLogger()
    print(id(logger1) == id(logger2))
    print(logger2.get_logs())

    # Subclass instance sharing
    handler1 = ErrorHandler()
    handler1.report("Initial error")
    handler2 = ErrorHandler()
    print(id(handler1) == id(handler2))
    print(handler2.errors)

    # Thread safety demonstration
    def thread_task():
        logger = CentralLogger()
        logger.log("Thread message")
        time.sleep(0.1)  # Simulate work

    import time
    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_task, name=f"Worker-{i}")
        t.start()
        threads.append(t)
    logger1.log("Before threads")
    for t in threads:
        t.join()
    print(CentralLogger().get_logs())

    # Pickling preservation
    pickled_data = pickle.dumps(logger1)
    logger3 = pickle.loads(pickled_data)
    print(id(logger3) == id(logger1))
    logger3.log("Post-pickle message")
    print(CentralLogger().get_logs()[-1])