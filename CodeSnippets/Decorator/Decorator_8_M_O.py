from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Service(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass
    @abstractmethod
    def execute(self, payload: Any) -> Any:
        pass

class BasicService(Service):
    def __init__(self, name: str):
        if not name:
            raise ValueError("name is required")
        self.name = name
    def get_description(self) -> str:
        return f"BasicService({self.name})"
    def execute(self, payload: Any) -> Any:
        if payload == "fail":
            raise RuntimeError("simulated failure")
        return f"{self.name} processed {payload}"

class ServiceWrapper(Service):
    def __init__(self, service: Service, active: bool = True):
        if not isinstance(service, Service):
            raise TypeError("service must implement Service")
        self._service = service
        self.active = active
    def get_description(self) -> str:
        return self._service.get_description()
    def execute(self, payload: Any) -> Any:
        return self._service.execute(payload)

class LoggingLayer(ServiceWrapper):
    def get_description(self) -> str:
        return f"{self._service.get_description()} + Logging"
    def execute(self, payload: Any) -> Any:
        if not self.active:
            return self._service.execute(payload)
        print(f"[LOG] entering: payload={payload}")
        result = self._service.execute(payload)
        print(f"[LOG] exiting: result={result}")
        return result

class RetryLayer(ServiceWrapper):
    def __init__(self, service: Service, retries: int = 2):
        super().__init__(service)
        if retries < 0:
            raise ValueError("retries must be non-negative")
        self.retries = retries
    def get_description(self) -> str:
        return f"{self._service.get_description()} + Retry({self.retries})"
    def execute(self, payload: Any) -> Any:
        attempts = 0
        last_exc: Optional[Exception] = None
        while attempts <= self.retries:
            try:
                return self._service.execute(payload)
            except Exception as e:
                last_exc = e
                attempts += 1
                print(f"[RETRY] attempt {attempts} failed: {e}")
        raise last_exc

class CacheLayer(ServiceWrapper):
    def __init__(self, service: Service):
        super().__init__(service)
        self._cache: Dict[Any, Any] = {}
    def get_description(self) -> str:
        return f"{self._service.get_description()} + Cache"
    def execute(self, payload: Any) -> Any:
        if payload in self._cache:
            return f"cached -> {self._cache[payload]}"
        result = self._service.execute(payload)
        self._cache[payload] = result
        return result

if __name__ == "__main__":
    core = BasicService("WorkerA")
    wrapped = LoggingLayer(RetryLayer(CacheLayer(core), retries=1))
    print("Service:", wrapped.get_description())
    print(wrapped.execute("task1"))
    print(wrapped.execute("task1"))
    try:
        print(wrapped.execute("fail"))
    except Exception as e:
        print("Final error:", e)