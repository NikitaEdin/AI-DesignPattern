import threading
import functools
from typing import Dict, Any, Optional

def single_instance(cls):
    instances: Dict[type, Any] = {}
    lock = threading.RLock()
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    get_instance._instances = instances
    get_instance._lock = lock
    return get_instance

class GlobalCounter:
    _instance: Optional['GlobalCounter'] = None
    _lock = threading.RLock()
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, initial_value: int = 0):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._value = initial_value
                    self._operations = 0
                    self._initialized = True
    
    def increment(self) -> int:
        with self._lock:
            self._value += 1
            self._operations += 1
            return self._value
    
    def decrement(self) -> int:
        with self._lock:
            self._value -= 1
            self._operations += 1
            return self._value
    
    def get_value(self) -> int:
        return self._value
    
    def get_stats(self) -> Dict[str, int]:
        return {'value': self._value, 'operations': self._operations}
    
    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None
            cls._initialized = False

@single_instance
class ConfigManager:
    def __init__(self, config_name: str = "default"):
        self.config_name = config_name
        self._settings: Dict[str, Any] = {}
        self._lock = threading.RLock()
    
    def set_setting(self, key: str, value: Any) -> None:
        with self._lock:
            self._settings[key] = value
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)
    
    def get_all_settings(self) -> Dict[str, Any]:
        return self._settings.copy()

if __name__ == "__main__":
    counter1 = GlobalCounter(10)
    counter2 = GlobalCounter(50)
    
    print(f"Counter1 value: {counter1.get_value()}")
    print(f"Counter2 value: {counter2.get_value()}")
    print(f"Same instance: {counter1 is counter2}")
    
    counter1.increment()
    print(f"After increment - Counter2 value: {counter2.get_value()}")
    
    config1 = ConfigManager("app_config")
    config2 = ConfigManager("db_config")
    
    config1.set_setting("database_url", "localhost:5432")
    config1.set_setting("debug", True)
    
    print(f"Config1 settings: {config1.get_all_settings()}")
    print(f"Config2 settings: {config2.get_all_settings()}")
    print(f"Same config instance: {config1 is config2}")
    
    def worker_thread(thread_id: int):
        counter = GlobalCounter()
        for _ in range(5):
            counter.increment()
        print(f"Thread {thread_id} final stats: {counter.get_stats()}")
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    final_counter = GlobalCounter()
    print(f"Final counter stats: {final_counter.get_stats()}")