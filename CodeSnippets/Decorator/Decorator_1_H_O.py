import abc
import threading
import contextlib
import datetime
import base64
from typing import Iterator

class ServiceABC(abc.ABC):
    @abc.abstractmethod
    def operation(self) -> str:
        raise NotImplementedError

class BaseService(ServiceABC):
    def __init__(self, name: str):
        self.name = name
    def operation(self) -> str:
        return f"[base:{self.name}]"

class ServiceWrapper(ServiceABC):
    def __init__(self, inner: ServiceABC, active: bool = True):
        if not isinstance(inner, ServiceABC):
            raise TypeError("inner must implement ServiceABC")
        self._inner = inner
        self._active = bool(active)
        self._lock = threading.RLock()
    def operation(self) -> str:
        result = self._inner.operation()
        with self._lock:
            return self.modify(result) if self._active else result
    def modify(self, data: str) -> str:
        return data
    def enable(self) -> None:
        with self._lock:
            self._active = True
    def disable(self) -> None:
        with self._lock:
            self._active = False
    def is_active(self) -> bool:
        with self._lock:
            return self._active
    @contextlib.contextmanager
    def temp_active(self, state: bool) -> Iterator[None]:
        with self._lock:
            prev = self._active
            self._active = bool(state)
        try:
            yield
        finally:
            with self._lock:
                self._active = prev
    def replace(self, new_inner: ServiceABC) -> None:
        if not isinstance(new_inner, ServiceABC):
            raise TypeError("new_inner must implement ServiceABC")
        with self._lock:
            self._inner = new_inner
    def __getattr__(self, name):
        return getattr(self._inner, name)
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} active={self._active} inner={repr(self._inner)}>"

class TimestampEnhancer(ServiceWrapper):
    def modify(self, data: str) -> str:
        ts = datetime.datetime.utcnow().isoformat(timespec='seconds') + "Z"
        return f"{ts} | {data}"

class Base64Enhancer(ServiceWrapper):
    def modify(self, data: str) -> str:
        if not isinstance(data, str):
            data = str(data)
        b = data.encode('utf-8')
        return base64.b64encode(b).decode('ascii')

if __name__ == "__main__":
    base = BaseService("Alpha")
    stamp = TimestampEnhancer(base)
    enc = Base64Enhancer(stamp)
    print("Chain result:", enc.operation())
    print("Underlying name via forwarding:", enc.name)
    stamp.disable()
    print("After disabling timestamp:", enc.operation())
    enc.disable()
    print("After disabling encoder:", enc.operation())
    enc.enable()
    with stamp.temp_active(True):
        print("Temporary enable timestamp:", enc.operation())
    new_base = BaseService("Beta")
    enc.replace(new_base)
    print("After replacing inner chain:", enc.operation())