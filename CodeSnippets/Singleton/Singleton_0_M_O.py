import threading
from typing import Any, Dict

class SingleInstanceMeta(type):
    _instances: Dict[type, object] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class AppConfigManager(metaclass=SingleInstanceMeta):
    def __init__(self, initial: Dict[str, Any] | None = None):
        self._lock = threading.RLock()
        self._config: Dict[str, Any] = {}
        if initial:
            if not isinstance(initial, dict):
                raise TypeError("initial configuration must be a dict")
            self._config.update(initial)

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._config[key] = value

    def reconfigure(self, new_config: Dict[str, Any]) -> None:
        if not isinstance(new_config, dict):
            raise TypeError("new_config must be a dict")
        with self._lock:
            self._config.clear()
            self._config.update(new_config)

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._config)

if __name__ == "__main__":
    manager_a = AppConfigManager({"mode": "production", "retry": 3})
    manager_b = AppConfigManager()

    print("IDs equal:", id(manager_a) == id(manager_b))
    print("Initial config:", manager_a.to_dict())

    manager_b.set("retry", 5)
    print("After update via manager_b:", manager_a.to_dict())

    try:
        manager_a.reconfigure({"mode": "staging", "debug": True})
    except TypeError as e:
        print("Configuration error:", e)

    print("Final config from manager_b:", manager_b.to_dict())