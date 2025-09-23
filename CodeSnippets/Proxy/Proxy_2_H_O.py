import threading
import time
import json
import hashlib
import random
from collections import OrderedDict

class ServiceInterface:
    def fetch(self, payload):
        raise NotImplementedError

class TransientError(Exception):
    pass

class PermanentError(Exception):
    pass

class RemoteService(ServiceInterface):
    def __init__(self):
        time.sleep(0.05)  # simulate startup
    @staticmethod
    def validate(payload):
        if payload is None:
            raise ValueError("payload required")
        if isinstance(payload, str) and payload == "":
            raise ValueError("empty payload not allowed")
    def fetch(self, payload):
        self.validate(payload)
        # simulate transient failures
        if payload == "bad":
            raise PermanentError("permanent rejection")
        if random.random() < 0.2:
            raise TransientError("temporary failure")
        return f"result:{payload}"

class StandIn(ServiceInterface):
    def __init__(self, auth_token, expected_token="secret", max_cache=64, retries=3, base_backoff=0.05):
        self._expected_token = expected_token
        self._token = auth_token
        self._real = None
        self._init_lock = threading.Lock()
        self._cache = OrderedDict()
        self._cache_lock = threading.RLock()
        self._in_flight = {}
        self._errors = {}
        self._max_cache = max_cache
        self._retries = retries
        self._base_backoff = base_backoff
        self._metrics = {"calls":0,"hits":0,"misses":0,"failures":0}
        self._metrics_lock = threading.Lock()
    def _ensure_real(self):
        if self._real is None:
            with self._init_lock:
                if self._real is None:
                    self._real = RemoteService()
    def _make_cache_key(self, payload):
        try:
            hash(("simple", payload))
            return ("simple", payload)
        except TypeError:
            try:
                s = json.dumps(payload, sort_keys=True, default=repr)
                h = hashlib.sha256(s.encode()).hexdigest()
                return ("json", h)
            except Exception:
                h = hashlib.sha256(repr(payload).encode()).hexdigest()
                return ("repr", h)
    def get_metrics(self):
        with self._metrics_lock:
            return dict(self._metrics)
    def _inc_metric(self, name, n=1):
        with self._metrics_lock:
            self._metrics[name] = self._metrics.get(name,0) + n
    def fetch(self, payload):
        RemoteService.validate(payload)  # align validation
        if self._token != self._expected_token:
            raise PermissionError("unauthorized")
        self._inc_metric("calls")
        key = self._make_cache_key(payload)
        with self._cache_lock:
            if key in self._cache:
                val = self._cache.pop(key)
                self._cache[key] = val
                self._inc_metric("hits")
                return val
            # register in-flight
            event = self._in_flight.get(key)
            if event is None:
                event = threading.Event()
                self._in_flight[key] = event
                is_caller = True
            else:
                is_caller = False
        if not is_caller:
            event.wait()
            with self._cache_lock:
                if key in self._cache:
                    self._inc_metric("hits")
                    return self._cache[key]
                err = self._errors.pop(key, None)
                if err:
                    raise err
                raise RuntimeError("unknown failure")
        # caller thread performs the work
        try:
            self._inc_metric("misses")
            self._ensure_real()
            last_exc = None
            for attempt in range(1, self._retries+1):
                try:
                    res = self._real.fetch(payload)
                    with self._cache_lock:
                        self._cache[key] = res
                        # enforce max size
                        while len(self._cache) > self._max_cache:
                            self._cache.popitem(last=False)
                    return res
                except TransientError as e:
                    last_exc = e
                    time.sleep(self._base_backoff * (2 ** (attempt-1)))
                    continue
                except Exception as e:
                    last_exc = e
                    break
            # exhausted retries or permanent error
            self._inc_metric("failures")
            raise last_exc
        except Exception as e:
            with self._cache_lock:
                self._errors[key] = e
            raise
        finally:
            with self._cache_lock:
                ev = self._in_flight.pop(key, None)
                if ev:
                    ev.set()

if __name__ == "__main__":
    s = StandIn(auth_token="secret")
    print(s.fetch("alpha"))
    print(s.fetch("alpha"))  # should hit cache
    try:
        s.fetch("")  # raises due to validation
    except Exception as e:
        print("validation:", type(e).__name__)
    # concurrent requests deduplication demo
    def worker(payload):
        try:
            print(threading.current_thread().name, s.fetch(payload))
        except Exception as e:
            print(threading.current_thread().name, "err", type(e).__name__)
    threads = [threading.Thread(target=worker, args=(["list","payload"],), name=f"T{i}") for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("metrics:", s.get_metrics())