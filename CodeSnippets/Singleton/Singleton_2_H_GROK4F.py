import threading
import copy

class InstanceEnforcer(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super(InstanceEnforcer, cls).__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]

class CentralLogger(metaclass=InstanceEnforcer):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._level = 'INFO'
        self._messages = []

    def set_level(self, level):
        self._level = level.upper()

    def log(self, message, level=None):
        if level is None:
            level = self._level
        self._messages.append(f"[{level}] {message}")

    def get_messages(self):
        return self._messages[:]

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        if id(self) not in memo:
            memo[id(self)] = self
        return self

if __name__ == "__main__":
    print("Creating first logger")
    l1 = CentralLogger()
    l1.log("First message")
    print("Creating second logger")
    l2 = CentralLogger()
    l2.log("Second message")
    print("Same instance:", id(l1) == id(l2))
    print("Messages:", l1.get_messages())

    def thread_log():
        l = CentralLogger()
        l.log(f"Thread {threading.current_thread().name} message")
        print(f"Thread {threading.current_thread().name} instance id: {id(l)}")

    t1 = threading.Thread(target=thread_log, name="T1")
    t2 = threading.Thread(target=thread_log, name="T2")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("All messages:", l1.get_messages())
    print("Final instance id:", id(l1))