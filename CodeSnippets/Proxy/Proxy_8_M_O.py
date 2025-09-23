from abc import ABC, abstractmethod
import time
import hashlib

class ServiceInterface(ABC):
    @abstractmethod
    def execute(self, payload: str) -> str:
        pass

class HeavyComputationService(ServiceInterface):
    def execute(self, payload: str) -> str:
        time.sleep(0.5)
        digest = hashlib.sha256(payload.encode()).hexdigest()
        return f"computed:{digest}"

class ServiceAccessManager(ServiceInterface):
    def __init__(self, valid_tokens=None):
        self._valid_tokens = set(valid_tokens or [])
        self._real_service = None
        self._cache = {}
        self._last_token = None

    def _ensure_service(self):
        if self._real_service is None:
            self._real_service = HeavyComputationService()

    def register_token(self, token: str):
        if not token or not isinstance(token, str):
            raise ValueError("token must be a non-empty string")
        self._valid_tokens.add(token)

    def execute(self, payload: str, token: str = None) -> str:
        if token is None:
            raise PermissionError("authentication token required")
        if token not in self._valid_tokens:
            raise PermissionError("invalid token")
        key = (token, payload)
        if key in self._cache:
            return f"cached:{self._cache[key]}"
        self._ensure_service()
        try:
            result = self._real_service.execute(payload)
        except Exception as exc:
            raise RuntimeError("service execution failed") from exc
        self._cache[key] = result
        self._last_token = token
        return result

if __name__ == "__main__":
    manager = ServiceAccessManager(valid_tokens=["alice-token"])
    try:
        print("Attempt without token:")
        print(manager.execute("data1"))
    except Exception as e:
        print("Error:", e)

    try:
        print("\nAttempt with invalid token:")
        print(manager.execute("data1", token="bob-token"))
    except Exception as e:
        print("Error:", e)

    print("\nValid calls:")
    print(manager.execute("data1", token="alice-token"))
    print("Second call (should be cached):")
    print(manager.execute("data1", token="alice-token"))
    print("\nNew payload:")
    print(manager.execute("data2", token="alice-token"))