import threading

class ResourceManager:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.resources = {'default': 'initial value'}
            self._counter = 1
            self._initialized = True

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None
            cls._initialized = False

    def add_resource(self, key, value):
        if key not in self.resources:
            self.resources[key] = value
            self._counter += 1

    def get_resource(self, key):
        return self.resources.get(key)

    def update_resource(self, key, value):
        if key in self.resources:
            self.resources[key] = value

    def remove_resource(self, key):
        if key in self.resources and key != 'default':
            del self.resources[key]
            self._counter -= 1
            if self._counter < 1:
                self._counter = 0

    def get_resource_count(self):
        return len(self.resources)

    def __repr__(self):
        return f"ResourceManager with {self._counter} resources"

def thread_task(thread_id, manager):
    key = f"key_{thread_id}"
    manager.add_resource(key, f"value_{thread_id}")
    print(f"Thread {thread_id}: Added {key}, count: {manager.get_resource_count()}")
    if thread_id == 1:
        manager.update_resource("default", "updated value")
    retrieved = manager.get_resource(key)
    print(f"Thread {thread_id}: Retrieved {retrieved}")
    if thread_id % 2 == 0:
        manager.remove_resource(key)
        print(f"Thread {thread_id}: Removed {key}, count: {manager.get_resource_count()}")

if __name__ == "__main__":
    manager1 = ResourceManager()
    print(f"Initial: {manager1}")
    print(f"ID: {id(manager1)}")
    print(f"Count: {manager1.get_resource_count()}")
    print(f"Default: {manager1.get_resource('default')}")

    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_task, args=(i+1, manager1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    manager2 = ResourceManager()
    print(f"Second instance ID: {id(manager2)}")
    print(f"Final: {manager2}")
    print(f"Count: {manager2.get_resource_count()}")
    print(f"Default: {manager2.get_resource('default')}")

    ResourceManager.reset_instance()
    manager3 = ResourceManager()
    print(f"Reset instance ID: {id(manager3)}")