import threading
import functools
from typing import Any, Dict, Optional

class ApplicationKernel:
    _instance: Optional['ApplicationKernel'] = None
    _lock = threading.RLock()
    _initialized = threading.Event()

    def __new__(cls, *args, **kwargs) -> 'ApplicationKernel':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        if self._initialized.is_set():
            return
        with self._lock:
            if self._initialized.is_set():
                return
            self.config = config or {}
            self._resources: Dict[str, Any] = {}
            self._initialized.set()

    def register(self, name: str, resource: Any) -> None:
        with self._lock:
            self._resources[name] = resource

    def retrieve(self, name: str) -> Any:
        with self._lock:
            return self._resources.get(name)

    def clear(self) -> None:
        with self._lock:
            self._resources.clear()

    @classmethod
    def reset_for_testing(cls) -> None:
        with cls._lock:
            cls._instance = None
            cls._initialized.clear()

    def __reduce__(self):
        return (self.__class__, (self.config,))

def synchronized_resource(name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kernel = ApplicationKernel()
            resource = kernel.retrieve(name)
            if resource is None:
                resource = func(*args, **kwargs)
                kernel.register(name, resource)
            return resource
        return wrapper
    return decorator

@synchronized_resource('logger')
def create_logger():
    class Logger:
        def __init__(self):
            self.entries = []
        def log(self, message: str) -> None:
            self.entries.append(message)
    return Logger()

if __name__ == "__main__":
    import concurrent.futures

    def worker_task(worker_id: int) -> int:
        kernel = ApplicationKernel({'debug': True})
        logger = create_logger()
        logger.log(f"Worker {worker_id} reporting")
        return id(kernel)

    kernel1 = ApplicationKernel({'env': 'prod'})
    kernel2 = ApplicationKernel({'env': 'dev'})

    assert kernel1 is kernel2
    assert kernel1.config['env'] == 'prod'

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(worker_task, range(5)))

    assert all(r == id(kernel1) for r in results)

    logger = create_logger()
    assert len(logger.entries) == 5
    assert all("Worker" in entry for entry in logger.entries)

    ApplicationKernel.reset_for_testing()
    new_kernel = ApplicationKernel({'reset': True})
    assert new_kernel is not kernel1