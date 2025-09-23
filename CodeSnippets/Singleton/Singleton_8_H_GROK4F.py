import threading
import time

class ResourceManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ResourceManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._data = {}
        self._counter = 0
        self._initialized = True

    def get_data(self, key):
        return self._data.get(key, None)

    def set_data(self, key, value):
        self._data[key] = value
        self._counter += 1

    def get_counter(self):
        return self._counter

    def reset(self):
        self._data.clear()
        self._counter = 0

    @classmethod
    def get_instance(cls):
        return cls()

def worker_thread(num):
    manager = ResourceManager()
    manager.set_data(f"thread_{num}", f"value_{num}")
    time.sleep(0.1)
    retrieved = manager.get_data(f"thread_{num}")
    print(f"Thread {num}: Retrieved {retrieved}, Counter: {manager.get_counter()}")
    return id(manager)

if __name__ == "__main__":
    print("Direct instance creation:")
    mgr1 = ResourceManager()
    mgr2 = ResourceManager()
    print(f"ID of mgr1: {id(mgr1)}")
    print(f"ID of mgr2: {id(mgr2)}")
    print(f"Same instance: {mgr1 is mgr2}")
    
    mgr1.set_data("test_key", "test_value")
    print(f"Retrieved from mgr2: {mgr2.get_data('test_key')}")
    
    print("\nThreaded access demonstration:")
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    final_mgr = ResourceManager()
    print(f"\nFinal counter value: {final_mgr.get_counter()}")
    print(f"Final instance ID: {id(final_mgr)}")