import threading
from typing import Any, Dict, Optional

class UniqueInstanceMeta(type):
    _instances: Dict[type, object] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class AppConfig(metaclass=UniqueInstanceMeta):
    def __init__(self, initial: Optional[Dict[str, Any]] = None):
        if not isinstance(initial, (type(None), dict)):
            raise TypeError("initial configuration must be a dict or None")
        self._lock = threading.RLock()
        self._data: Dict[str, Any] = {}
        if initial:
            self._data.update(initial)

    def get_value(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(key, default)

    def set_value(self, key: str, value: Any) -> None:
        with self._lock:
            if key is None:
                raise ValueError("key must not be None")
            self._data[key] = value

    def update_values(self, updates: Dict[str, Any]) -> None:
        if not isinstance(updates, dict):
            raise TypeError("updates must be a dict")
        with self._lock:
            self._data.update(updates)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self.to_dict()})"


def _worker(name: str):
    cfg = AppConfig()
    print(f"Worker {name}: id={id(cfg)} data={cfg.to_dict()}")


if __name__ == "__main__":
    try:
        AppConfig("not-a-dict")
    except Exception as err:
        print("Initialization error:", err)

    config_a = AppConfig({"host": "127.0.0.1"})
    config_b = AppConfig()
    print("Instances are identical:", id(config_a) == id(config_b))
    print("Initial config:", config_a.to_dict())

    config_b.set_value("port", 8080)
    print("After update via second reference:", config_a.to_dict())

    threads = []
    for i in range(4):
        t = threading.Thread(target=_worker, args=(f"T{i+1}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()