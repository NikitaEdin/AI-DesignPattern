import threading
import time
from typing import Any, Optional

class SharedResource:
    _instance: Optional['SharedResource'] = None
    _lock = threading.RLock()
    
    def __new__(cls, *args: Any, **kwargs: Any) -> 'SharedResource':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, initial_value: int = 0) -> None:
        if self._initialized:
            return
        self._value = initial_value
        self._access_count = 0
        self._lock = threading.RLock()
        self._initialized = True
    
    def update_value(self, new_value: int) -> None:
        with self._lock:
            self._value = new_value
            self._access_count += 1
    
    def get_value(self) -> int:
        with self._lock:
            self._access_count += 1
            return self._value
    
    def get_stats(self) -> dict:
        with self._lock:
            return {
                'current_value': self._value,
                'access_count': self._access_count,
                'instance_id': id(self)
            }
    
    def __reduce__(self):
        return (self.__class__, (self._value,))
    
    def __copy__(self):
        return self
    
    def __deepcopy__(self, memo):
        return self
    
    def __bool__(self):
        return True
    
    def __repr__(self):
        return f"<SharedResource(id={id(self)}, value={self._value})>"

if __name__ == '__main__':
    def worker_thread(thread_id: int) -> None:
        resource = SharedResource(thread_id * 10)
        time.sleep(0.001)
        stats = resource.get_stats()
        print(f"Thread {thread_id}: {stats}")
    
    print("Instance 1:", SharedResource(100))
    print("Instance 2:", SharedResource(200))
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    final = SharedResource()
    print("\nFinal stats:", final.get_stats())