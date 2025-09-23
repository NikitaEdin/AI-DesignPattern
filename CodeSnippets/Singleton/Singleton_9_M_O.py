import threading
import json
import tempfile
import os

class UniqueInstanceMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with UniqueInstanceMeta._lock:
            if cls in UniqueInstanceMeta._instances:
                return UniqueInstanceMeta._instances[cls]
            try:
                instance = super().__call__(*args, **kwargs)
            except Exception:
                UniqueInstanceMeta._instances.pop(cls, None)
                raise
            UniqueInstanceMeta._instances[cls] = instance
            return instance

class GlobalConfig(metaclass=UniqueInstanceMeta):
    def __init__(self, config_data=None, config_path=None):
        self._data = {}
        if config_path:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception as e:
                raise ValueError(f"Unable to load config from path: {e}")
        if config_data:
            if not isinstance(config_data, dict):
                raise TypeError("config_data must be a dict")
            self._data.update(config_data)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def as_dict(self):
        return dict(self._data)

if __name__ == "__main__":
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    try:
        temp.write(json.dumps({"app": "demo", "version": 1}).encode("utf-8"))
        temp.close()

        cfg_a = GlobalConfig(config_path=temp.name)
        cfg_b = GlobalConfig(config_data={"added": True})

        print("same_object:", cfg_a is cfg_b)
        print("ids:", id(cfg_a), id(cfg_b))
        print("app value:", cfg_b.get("app"))
        print("added value:", cfg_a.get("added"))
        cfg_b.set("new_key", 123)
        print("new_key via cfg_a:", cfg_a.get("new_key"))
        print("full config:", cfg_a.as_dict())
    finally:
        os.unlink(temp.name)