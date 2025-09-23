import threading
import weakref
from functools import wraps


def synchronized(lock):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator


class ConfigurationManager:
    _instance = None
    _instances = weakref.WeakSet()
    _lock = threading.RLock()
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instances.add(cls._instance)
        return cls._instance
    
    @synchronized(_lock)
    def __init__(self, config_data=None):
        if not self._initialized:
            self._config = config_data or {}
            self._observers = []
            self._version = 1
            self._initialized = True
    
    @synchronized(_lock)
    def set_config(self, key, value):
        old_value = self._config.get(key)
        if old_value != value:
            self._config[key] = value
            self._version += 1
            self._notify_observers(key, old_value, value)
    
    def get_config(self, key, default=None):
        return self._config.get(key, default)
    
    @synchronized(_lock)
    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    @synchronized(_lock)
    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, key, old_value, new_value):
        for observer in self._observers:
            try:
                observer(key, old_value, new_value)
            except Exception:
                pass
    
    @property
    def version(self):
        return self._version
    
    @classmethod
    @synchronized(_lock)
    def reset_instance(cls):
        cls._instance = None
        cls._initialized = False
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={id(self)} config_count={len(self._config)}>"


def config_change_handler(key, old_value, new_value):
    print(f"Config changed: {key} = {old_value} -> {new_value}")


if __name__ == "__main__":
    import concurrent.futures
    
    def create_manager(thread_id):
        manager = ConfigurationManager({"thread_id": thread_id, "initial": True})
        return id(manager), manager.get_config("thread_id")
    
    manager1 = ConfigurationManager({"database_url": "localhost", "debug": True})
    manager2 = ConfigurationManager({"api_key": "secret"})
    
    print(f"Same instance: {manager1 is manager2}")
    print(f"Manager1 config: {manager1.get_config('database_url')}")
    print(f"Manager2 config: {manager2.get_config('database_url')}")
    
    manager1.add_observer(config_change_handler)
    manager1.set_config("timeout", 30)
    manager2.set_config("max_connections", 100)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_manager, i) for i in range(5)]
        results = [future.result() for future in futures]
    
    print("Thread safety test - all instances should have same ID:")
    for instance_id, thread_id in results:
        print(f"Thread {thread_id}: Instance ID {instance_id}")
    
    print(f"Final config version: {manager1.version}")
    ConfigurationManager.reset_instance()