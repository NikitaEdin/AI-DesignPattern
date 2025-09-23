from abc import ABC, abstractmethod
import time

class DataProvider(ABC):
    @abstractmethod
    def get_data(self, key: str) -> str:
        pass

class RemoteDatabase(DataProvider):
    def __init__(self):
        time.sleep(0.2)
        self._store = {
            "alpha": "Value for alpha",
            "beta": "Value for beta",
            "gamma": "Value for gamma"
        }

    def get_data(self, key: str) -> str:
        if key not in self._store:
            raise KeyError(f"Key not found: {key}")
        time.sleep(0.1)
        return self._store[key]

class AccessController(DataProvider):
    def __init__(self, user: str, allowed: set):
        self._user = user
        self._allowed = allowed
        self._real = None
        self._cache = {}

    def _ensure_real(self):
        if self._real is None:
            try:
                self._real = RemoteDatabase()
            except Exception as e:
                raise RuntimeError("Failed to initialize data source") from e

    def get_data(self, key: str) -> str:
        if self._user not in self._allowed:
            raise PermissionError("User is not authorized to access data")
        if key in self._cache:
            return self._cache[key]
        self._ensure_real()
        try:
            value = self._real.get_data(key)
        except KeyError as e:
            raise ValueError(str(e)) from e
        self._cache[key] = value
        return value

if __name__ == "__main__":
    allowed_users = {"alice", "bob"}
    controller_alice = AccessController("alice", allowed_users)
    controller_eve = AccessController("eve", allowed_users)

    try:
        print(controller_alice.get_data("alpha"))
        print(controller_alice.get_data("alpha"))
        print(controller_alice.get_data("beta"))
    except Exception as exc:
        print("Error for alice:", exc)

    try:
        print(controller_eve.get_data("alpha"))
    except Exception as exc:
        print("Error for eve:", exc)