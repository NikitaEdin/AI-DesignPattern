from abc import ABC, abstractmethod
from typing import Optional, Callable, Dict


class ServiceInterface(ABC):
    @abstractmethod
    def fetch(self, resource_id: str, token: Optional[str] = None) -> Dict:
        pass


class RealService(ServiceInterface):
    def __init__(self):
        self._data_store = {
            "1": {"id": "1", "value": "Alpha"},
            "2": {"id": "2", "value": "Beta"},
            "3": {"id": "3", "value": "Gamma"},
        }

    def fetch(self, resource_id: str, token: Optional[str] = None) -> Dict:
        if resource_id not in self._data_store:
            raise KeyError(f"Resource '{resource_id}' not found")
        return self._data_store[resource_id]


class ServiceController(ServiceInterface):
    def __init__(self, validator: Callable[[Optional[str]], bool]):
        self._validator = validator
        self._real: Optional[RealService] = None
        self._cache: Dict[str, Dict] = {}

    def _ensure_real(self) -> None:
        if self._real is None:
            self._real = RealService()

    def fetch(self, resource_id: str, token: Optional[str] = None) -> Dict:
        if not self._validator(token):
            raise PermissionError("Invalid access token")
        if resource_id in self._cache:
            return self._cache[resource_id]
        self._ensure_real()
        try:
            result = self._real.fetch(resource_id)
        except Exception as err:
            raise RuntimeError(f"Failed to retrieve resource '{resource_id}': {err}") from err
        self._cache[resource_id] = result
        return result


def main():
    def token_checker(t: Optional[str]) -> bool:
        return t == "valid-token"

    controller = ServiceController(token_checker)

    try:
        controller.fetch("1", token="invalid")
    except PermissionError as e:
        print("Access denied:", e)

    try:
        data = controller.fetch("1", token="valid-token")
        print("First fetch:", data)
        cached = controller.fetch("1", token="valid-token")
        print("Second fetch (cached):", cached)
        controller.fetch("999", token="valid-token")
    except Exception as e:
        print("Error during operations:", e)


if __name__ == "__main__":
    main()