import time
import threading
from abc import ABC, abstractmethod
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

class ServiceInterface(ABC):
    @abstractmethod
    def get_resource(self, resource_id: str) -> str:
        pass

    @abstractmethod
    def compute(self, x: int) -> int:
        pass

class RealService(ServiceInterface):
    def __init__(self):
        self._startup_time = time.time()

    def get_resource(self, resource_id: str) -> str:
        time.sleep(0.2)
        return f"resource:{resource_id}@{int(self._startup_time)}"

    def compute(self, x: int) -> int:
        time.sleep(0.1)
        return x * x

class ControlledAccess(ServiceInterface):
    def __init__(self, credentials: dict, allowed_users: dict, max_cache=128, ttl=5.0, max_attempts=3, lockout_time=10):
        self._credentials = credentials
        self._allowed = allowed_users
        self._max_attempts = max_attempts
        self._lockout_time = lockout_time
        self._failed_attempts = {}
        self._lockouts = {}
        self._real_instance = None
        self._instance_lock = threading.RLock()
        self._cache = OrderedDict()
        self._cache_lock = threading.RLock()
        self._max_cache = max_cache
        self._ttl = ttl

    def _check_auth(self):
        user = self._credentials.get("user")
        pwd = self._credentials.get("password")
        now = time.time()
        if user in self._lockouts and now < self._lockouts[user]:
            raise PermissionError("account locked")
        expected = self._allowed.get(user)
        if expected is None or expected != pwd:
            self._failed_attempts[user] = self._failed_attempts.get(user, 0) + 1
            if self._failed_attempts[user] >= self._max_attempts:
                self._lockouts[user] = now + self._lockout_time
                self._failed_attempts[user] = 0
            raise PermissionError("invalid credentials")
        self._failed_attempts[user] = 0
        return True

    def _ensure_real(self):
        if self._real_instance is None:
            with self._instance_lock:
                if self._real_instance is None:
                    self._real_instance = RealService()
        return self._real_instance

    def _cache_get(self, key):
        with self._cache_lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            value, expiry = entry
            if time.time() > expiry:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return value

    def _cache_set(self, key, value):
        with self._cache_lock:
            expiry = time.time() + self._ttl
            self._cache[key] = (value, expiry)
            self._cache.move_to_end(key)
            while len(self._cache) > self._max_cache:
                self._cache.popitem(last=False)

    def get_resource(self, resource_id: str) -> str:
        self._check_auth()
        key = f"res:{resource_id}"
        cached = self._cache_get(key)
        if cached is not None:
            return f"{cached} (cached)"
        real = self._ensure_real()
        try:
            value = real.get_resource(resource_id)
        except Exception as e:
            cached_fallback = self._cache_get(key)
            if cached_fallback is not None:
                return f"{cached_fallback} (fallback)"
            raise RuntimeError("real service failed") from e
        self._cache_set(key, value)
        return value

    def compute(self, x: int) -> int:
        self._check_auth()
        key = f"compute:{x}"
        cached = self._cache_get(key)
        if cached is not None:
            return cached
        real = self._ensure_real()
        result = real.compute(x)
        self._cache_set(key, result)
        return result

if __name__ == "__main__":
    allowed = {"alice": "wonderland", "bob": "builder"}
    creds = {"user": "alice", "password": "wrong"}
    actor = ControlledAccess(creds, allowed, max_cache=16, ttl=2.0, max_attempts=2, lockout_time=5)

    try:
        actor.get_resource("alpha")
    except PermissionError as e:
        print("Auth failed:", e)

    creds["password"] = "wonderland"
    try:
        print("First fetch:", actor.get_resource("alpha"))
        print("Second fetch:", actor.get_resource("alpha"))
        print("Compute 5:", actor.compute(5))
        print("Compute 5 cached:", actor.compute(5))
    except Exception as e:
        print("Error:", e)

    def task(n):
        try:
            return actor.compute(n)
        except Exception as e:
            return f"err:{e}"

    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(task, i % 6) for i in range(12)]
        for f in as_completed(futures):
            print("Concurrent result:", f.result())

    time.sleep(3)
    print("After TTL expired, fetch:", actor.get_resource("alpha"))