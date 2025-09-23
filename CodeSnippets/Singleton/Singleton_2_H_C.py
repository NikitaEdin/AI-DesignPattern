import threading
import weakref
from functools import wraps

def _synchronized(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return func(self, *args, **kwargs)
    return wrapper

class MetaUniqueInstance(type):
    _instances = {}
    _lock = threading.RLock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]
    
    def clear_instances(cls):
        with cls._lock:
            if cls in cls._instances:
                del cls._instances[cls]

class DatabaseConnection(metaclass=MetaUniqueInstance):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._lock = threading.RLock()
        self._connection_pool = []
        self._connected = False
        self._observers = weakref.WeakSet()
        self._initialized = True
    
    @_synchronized
    def connect(self, host="localhost", port=5432):
        if not self._connected:
            self._host = host
            self._port = port
            self._connected = True
            self._notify_observers("connected")
    
    @_synchronized
    def disconnect(self):
        if self._connected:
            self._connection_pool.clear()
            self._connected = False
            self._notify_observers("disconnected")
    
    @_synchronized
    def execute_query(self, query):
        if not self._connected:
            raise RuntimeError("Database not connected")
        return f"Executing: {query} on {self._host}:{self._port}"
    
    def add_observer(self, observer):
        self._observers.add(observer)
    
    def _notify_observers(self, event):
        for observer in self._observers:
            if hasattr(observer, 'on_connection_event'):
                observer.on_connection_event(event)
    
    @property
    def is_connected(self):
        return self._connected
    
    def __copy__(self):
        return self
    
    def __deepcopy__(self, memo):
        return self

class ConnectionObserver:
    def __init__(self, name):
        self.name = name
    
    def on_connection_event(self, event):
        print(f"Observer {self.name} notified: {event}")

def worker_thread(thread_id):
    db = DatabaseConnection()
    db.connect(f"server_{thread_id}", 5432 + thread_id)
    result = db.execute_query(f"SELECT * FROM table_{thread_id}")
    return id(db), result

if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")
    print(f"Instance ID: {id(db1)}")
    
    observer1 = ConnectionObserver("Monitor1")
    observer2 = ConnectionObserver("Monitor2")
    
    db1.add_observer(observer1)
    db1.add_observer(observer2)
    
    db1.connect("production-server", 5432)
    print(f"Connected: {db1.is_connected}")
    print(db1.execute_query("SELECT * FROM users"))
    
    import threading
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker_thread, i) for i in range(3)]
        results = [future.result() for future in futures]
    
    print("Thread results:")
    for i, (instance_id, query_result) in enumerate(results):
        print(f"Thread {i}: ID={instance_id}, Same as main: {instance_id == id(db1)}")
    
    db1.disconnect()
    
    import copy
    db3 = copy.copy(db1)
    db4 = copy.deepcopy(db1)
    print(f"Copy protection: {db1 is db3 is db4}")