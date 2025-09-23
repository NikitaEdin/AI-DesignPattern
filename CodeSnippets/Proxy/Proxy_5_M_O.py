import time
import random
from abc import ABC, abstractmethod

class DataServiceBase(ABC):
    @abstractmethod
    def get_data(self, key: str) -> str:
        pass

class RealDataService(DataServiceBase):
    def get_data(self, key: str) -> str:
        if not key:
            raise ValueError("Key must be non-empty")
        time.sleep(0.4)
        if key == "error":
            raise RuntimeError("Simulated backend failure")
        return f"data_for_{key}_{random.randint(1000,9999)}"

class AccessError(Exception):
    pass

class RetrievalError(Exception):
    pass

class DataGateway(DataServiceBase):
    def __init__(self, token: str, max_calls: int = 10):
        self._valid_tokens = {"token123", "admin-token"}
        self._token = token
        self._service = None
        self._cache: dict[str, str] = {}
        self._calls = 0
        self._max_calls = max_calls

    def _ensure_service(self):
        if self._service is None:
            self._service = RealDataService()

    def _check_access(self):
        if self._token not in self._valid_tokens:
            raise AccessError("Invalid authentication token")
        if self._calls >= self._max_calls:
            raise AccessError("Call limit exceeded")

    def get_data(self, key: str) -> str:
        try:
            self._check_access()
        except AccessError:
            raise
        self._calls += 1
        if key in self._cache:
            return self._cache[key]
        try:
            self._ensure_service()
            result = self._service.get_data(key)
            self._cache[key] = result
            return result
        except Exception as exc:
            raise RetrievalError(f"Failed to retrieve '{key}': {exc}") from exc

if __name__ == "__main__":
    gateway = DataGateway("token123", max_calls=5)
    try:
        a = gateway.get_data("alpha")
        print("First fetch:", a)
        b = gateway.get_data("alpha")
        print("Cached fetch:", b)
        c = gateway.get_data("beta")
        print("Another key:", c)
        try:
            gateway.get_data("error")
        except RetrievalError as e:
            print("Handled retrieval error:", e)
        for i in range(3):
            print("Call", i+1, gateway.get_data(f"k{i}"))
    except AccessError as e:
        print("Access denied:", e)

    try:
        bad_gateway = DataGateway("bad-token")
        bad_gateway.get_data("alpha")
    except AccessError as e:
        print("Invalid token handled:", e)