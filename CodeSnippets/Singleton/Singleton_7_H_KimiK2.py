import threading
from typing import Any, Dict, Optional

class AppOrchestrator:
    _lock = threading.RLock()
    _instance: Optional['AppOrchestrator'] = None
    _initialized = False

    def __new__(cls, *args, **kwargs) -> 'AppOrchestrator':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Dict[str, Any] = None) -> None:
        if self._initialized:
            return
        with self._lock:
            if self._initialized:
                return
            self._config = config or {}
            self._resources: Dict[str, Any] = {}
            self._closed = False
            self._initialized = True

    def configure(self, **kwargs) -> None:
        with self._lock:
            if self._closed:
                raise RuntimeError("Instance is shutting down")
            self._config.update(kwargs)

    def get_resource(self, name: str) -> Any:
        with self._lock:
            if self._closed:
                raise RuntimeError("Instance is shutting down")
            return self._resources.get(name)

    def register_resource(self, name: str, resource: Any) -> None:
        with self._lock:
            if self._closed:
                raise RuntimeError("Instance is shutting down")
            if name in self._resources:
                raise ValueError(f"Resource '{name}' already registered")
            self._resources[name] = resource

    def shutdown(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
            for name, resource in list(self._resources.items()):
                if hasattr(resource, 'close'):
                    resource.close()
                del self._resources[name]

    @property
    def is_active(self) -> bool:
        return not self._closed

    def __del__(self):
        self.shutdown()

if __name__ == "__main__":
    import concurrent.futures

    def worker(n: int) -> str:
        inst = AppOrchestrator({'worker_id': n})
        return f"Worker {n}: {id(inst)}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(worker, range(5)))
    
    core = AppOrchestrator()
    core.register_resource('logger', type('Logger', (), {'close': lambda: None})())
    print("All workers see same instance:", all(r.split()[-1] == str(id(core)) for r in results))
    print("Resources:", list(core._resources.keys()))
    core.shutdown()