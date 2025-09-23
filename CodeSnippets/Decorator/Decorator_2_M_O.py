from abc import ABC, abstractmethod

class ServiceError(Exception):
    pass

class ServiceInterface(ABC):
    @abstractmethod
    def execute(self, payload: str) -> str:
        pass

class BasicProcessor(ServiceInterface):
    def execute(self, payload: str) -> str:
        if payload == "fail":
            raise ValueError("invalid payload")
        return f"Processed: {payload}"

class WrapperBase(ServiceInterface):
    def __init__(self, service: ServiceInterface, enabled: bool = True):
        if not isinstance(service, ServiceInterface):
            raise TypeError("service must implement ServiceInterface")
        self._service = service
        self.enabled = enabled
    def execute(self, payload: str) -> str:
        if not self.enabled:
            return self._service.execute(payload)
        try:
            return self._service.execute(payload)
        except Exception as exc:
            raise ServiceError("execution error") from exc

class LoggingLayer(WrapperBase):
    def __init__(self, service: ServiceInterface, enabled: bool = True, logger=None):
        super().__init__(service, enabled)
        self._logger = logger or print
    def execute(self, payload: str) -> str:
        if not self.enabled:
            return super().execute(payload)
        self._logger(f"-> start: {payload}")
        result = super().execute(payload)
        self._logger(f"<- end: {payload} => {result}")
        return result

class CacheLayer(WrapperBase):
    def __init__(self, service: ServiceInterface, enabled: bool = True):
        super().__init__(service, enabled)
        self._cache = {}
    def execute(self, payload: str) -> str:
        if not self.enabled:
            return super().execute(payload)
        key = payload
        if key in self._cache:
            return self._cache[key]
        result = super().execute(payload)
        self._cache[key] = result
        return result

if __name__ == "__main__":
    core = BasicProcessor()
    logged = LoggingLayer(core)
    cached_and_logged = CacheLayer(logged)
    print(cached_and_logged.execute("hello"))
    print(cached_and_logged.execute("hello"))
    logged.enabled = False
    print(cached_and_logged.execute("world"))
    try:
        print(cached_and_logged.execute("fail"))
    except ServiceError as e:
        print("Handled service error:", e)