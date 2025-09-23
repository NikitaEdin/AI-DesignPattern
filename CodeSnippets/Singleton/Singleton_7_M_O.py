import threading
from typing import Any, Dict, Optional

class GlobalConfig:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, initial: Optional[Dict[str, Any]] = None):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._data: Dict[str, Any] = {}
        self._data_lock = threading.RLock()
        if initial is not None:
            if not isinstance(initial, dict):
                raise TypeError("initial must be a dict")
            with self._data_lock:
                self._data.update(initial)

    def set_value(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        with self._data_lock:
            self._data[key] = value

    def get_value(self, key: str, default: Any = None) -> Any:
        with self._data_lock:
            return self._data.get(key, default)

    def remove_value(self, key: str) -> None:
        with self._data_lock:
            if key not in self._data:
                raise KeyError(f"Key '{key}' does not exist")
            del self._data[key]

    def all_values(self) -> Dict[str, Any]:
        with self._data_lock:
            return dict(self._data)

    def __repr__(self) -> str:
        return f"<GlobalConfig id={id(self)} keys={list(self._data.keys())}>"

def _worker(name: str, value: Any):
    cfg = GlobalConfig()
    cfg.set_value(name, value)
    print(f"Worker set {name}={value} on instance id={id(cfg)}")

if __name__ == "__main__":
    cfg1 = GlobalConfig({"app": "demo", "version": "1.0"})
    cfg2 = GlobalConfig()
    print(cfg1)
    print("Same instance:", cfg1 is cfg2)

    cfg1.set_value("debug", True)
    print("debug via cfg2:", cfg2.get_value("debug"))

    threads = []
    for i in range(4):
        t = threading.Thread(target=_worker, args=(f"thread_key_{i}", i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Final values:", cfg1.all_values())

    try:
        cfg1.remove_value("nonexistent")
    except KeyError as e:
        print("Expected error:", e)