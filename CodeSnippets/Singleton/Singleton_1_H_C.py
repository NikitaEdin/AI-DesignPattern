import threading
from collections import defaultdict

class UniqueInstance:
    _instances = {}
    _locks = defaultdict(threading.RLock)
    _initialized = defaultdict(bool)
    _instance_counts = defaultdict(int)
    
    def __new__(cls):
        if cls not in cls._instances:
            with cls._locks[cls]:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__new__(cls)
                    cls._instance_counts[cls] += 1
        return cls._instances[cls]
    
    def __init__(self):
        cls = self.__class__
        if not self._initialized[cls]:
            with self._locks[cls]:
                if not self._initialized[cls]:
                    self._setup()
                    self._initialized[cls] = True
    
    def _setup(self):
        pass
    
    @classmethod
    def get_instance_count(cls):
        return cls._instance_counts[cls]
    
    @classmethod
    def reset_instance(cls):
        with cls._locks[cls]:
            if cls in cls._instances:
                del cls._instances[cls]
                cls._initialized[cls] = False
                cls._instance_counts[cls] = 0

class DatabaseManager(UniqueInstance):
    def _setup(self):
        self.connection = "Database connection established"
        self.query_count = 0
        self._lock = threading.RLock()
    
    def execute_query(self, query):
        with self._lock:
            self.query_count += 1
            return f"Executing: {query} (Query #{self.query_count})"
    
    def get_stats(self):
        with self._lock:
            return f"Total queries: {self.query_count}"

class CacheManager(UniqueInstance):
    def _setup(self):
        self.cache = {}
        self.hit_count = 0
        self.miss_count = 0
        self._lock = threading.RLock()
    
    def get(self, key):
        with self._lock:
            if key in self.cache:
                self.hit_count += 1
                return self.cache[key]
            else:
                self.miss_count += 1
                return None
    
    def set(self, key, value):
        with self._lock:
            self.cache[key] = value
    
    def get_stats(self):
        with self._lock:
            total = self.hit_count + self.miss_count
            hit_rate = self.hit_count / total * 100 if total > 0 else 0
            return f"Hit rate: {hit_rate:.1f}% ({self.hit_count}/{total})"

def worker_function(manager_class, results, worker_id):
    instance = manager_class()
    results[worker_id] = id(instance)

if __name__ == "__main__":
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    print(f"DB managers same instance: {db1 is db2}")
    print(f"DB instance count: {DatabaseManager.get_instance_count()}")
    
    cache1 = CacheManager()
    cache2 = CacheManager()
    print(f"Cache managers same instance: {cache1 is cache2}")
    print(f"Cache instance count: {CacheManager.get_instance_count()}")
    
    print(f"Different classes, different instances: {db1 is not cache1}")
    
    print(db1.execute_query("SELECT * FROM users"))
    print(db1.execute_query("SELECT * FROM orders"))
    print(db1.get_stats())
    
    cache1.set("user:1", {"name": "Alice"})
    print(f"Cache get existing: {cache1.get('user:1')}")
    print(f"Cache get missing: {cache1.get('user:2')}")
    print(cache1.get_stats())
    
    results = {}
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker_function, args=(DatabaseManager, results, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    all_same = len(set(results.values())) == 1
    print(f"Thread safety test - all instances identical: {all_same}")
    
    DatabaseManager.reset_instance()
    db3 = DatabaseManager()
    print(f"After reset, new instance created: {db1 is not db3}")