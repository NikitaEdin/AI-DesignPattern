import threading
import concurrent.futures
import time

class IncompatibleMappingError(Exception):
    pass

class ServiceExecutionError(Exception):
    pass

class ServiceTimeoutError(Exception):
    pass

class UnifiedClient:
    def __init__(self, service, action_map, timeout=None, max_workers=4):
        self._service = service
        self._action_map = {}
        self._lock = threading.RLock()
        self._timeout = timeout
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self._validate_and_register(action_map)

    def _validate_and_register(self, action_map):
        if not isinstance(action_map, dict):
            raise IncompatibleMappingError("action_map must be a dict")
        allowed_methods = set()
        for action, descriptor in action_map.items():
            if not isinstance(action, str):
                raise IncompatibleMappingError("action keys must be strings")
            if not isinstance(descriptor, dict):
                raise IncompatibleMappingError("mapping descriptor must be a dict")
            method_name = descriptor.get("method")
            param_builder = descriptor.get("param_builder")
            if not isinstance(method_name, str):
                raise IncompatibleMappingError("method name must be a string")
            if not callable(param_builder):
                raise IncompatibleMappingError(f"param_builder for {action} must be callable")
            method = getattr(self._service, method_name, None)
            if method is None or not callable(method):
                raise IncompatibleMappingError(f"service has no callable method '{method_name}' for action '{action}'")
            # Try a safe dry-run of param_builder to validate return shape when possible
            try:
                sample = param_builder()
            except TypeError:
                sample = None
            if sample is not None:
                if not (isinstance(sample, (tuple, list)) and len(sample) == 2 and isinstance(sample[1], dict)):
                    raise IncompatibleMappingError(f"param_builder for '{action}' must return (args, kwargs)")
            self._action_map[action] = (method_name, param_builder)
            allowed_methods.add(method_name)
        self._allowed_methods = allowed_methods

    def perform(self, action, **kwargs):
        if action not in self._action_map:
            raise IncompatibleMappingError(f"Unknown action '{action}'")
        method_name, param_builder = self._action_map[action]
        try:
            built = param_builder(**kwargs)
        except Exception as exc:
            raise IncompatibleMappingError(f"param_builder error for '{action}': {exc}") from exc
        if not (isinstance(built, (tuple, list)) and len(built) == 2):
            raise IncompatibleMappingError(f"param_builder for '{action}' must return (args, kwargs)")
        args, kwo = built
        args = tuple(args) if args is not None else ()
        kwo = dict(kwo) if kwo is not None else {}
        method = getattr(self._service, method_name)
        future = self._executor.submit(self._invoke_safe, method, args, kwo)
        try:
            return future.result(timeout=self._timeout)
        except concurrent.futures.TimeoutError as exc:
            future.cancel()
            raise ServiceTimeoutError(f"call to '{method_name}' timed out") from exc
        except Exception as exc:
            raise ServiceExecutionError(f"error executing '{method_name}': {exc}") from exc

    def _invoke_safe(self, method, args, kwargs):
        with self._lock:
            return method(*args, **kwargs)

    def __getattr__(self, name):
        if name in self._allowed_methods:
            target = getattr(self._service, name)
            if callable(target):
                def wrapper(*a, **k):
                    future = self._executor.submit(self._invoke_safe, target, a, k)
                    try:
                        return future.result(timeout=self._timeout)
                    except concurrent.futures.TimeoutError as exc:
                        future.cancel()
                        raise ServiceTimeoutError(f"call to '{name}' timed out") from exc
                    except Exception as exc:
                        raise ServiceExecutionError(f"error executing '{name}': {exc}") from exc
                return wrapper
        raise AttributeError(name)

if __name__ == "__main__":
    class ModernService:
        def run(self, payload):
            return {"status": "ok", "processed": payload}

    class LegacyService:
        def execute(self, data, meta=None):
            return f"legacy:{data}:{meta}"

    class SlowService:
        def work(self, x):
            time.sleep(2)
            return x * 2

    modern = ModernService()
    legacy = LegacyService()
    slow = SlowService()

    action_map_modern = {
        "create": {"method": "run", "param_builder": lambda **kw: ((kw.get("payload"),), {})}
    }
    action_map_legacy = {
        "create": {"method": "execute", "param_builder": lambda **kw: ((), {"data": kw.get("payload"), "meta": kw.get("meta")})}
    }
    client_modern = UnifiedClient(modern, action_map_modern, timeout=1)
    client_legacy = UnifiedClient(legacy, action_map_legacy, timeout=1)
    client_slow = UnifiedClient(slow, {"double": {"method": "work", "param_builder": lambda **kw: ((kw.get("x"),), {})}}, timeout=0.5)

    print(client_modern.perform("create", payload="data123"))
    print(client_legacy.perform("create", payload="x", meta="m"))
    try:
        print(client_slow.perform("double", x=5))
    except ServiceTimeoutError as e:
        print("timeout occurred:", e)