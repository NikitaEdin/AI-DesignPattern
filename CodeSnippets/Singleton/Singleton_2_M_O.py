import threading

class GlobalConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, initial=None):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._data = {}
        if initial is not None:
            if not isinstance(initial, dict):
                raise TypeError("initial must be a dict")
            self._data.update(initial)

    def get_value(self, key, default=None):
        return self._data.get(key, default)

    def set_value(self, key, value):
        if key is None:
            raise ValueError("key cannot be None")
        self._data[key] = value

    def load_from_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        self._data[k.strip()] = v.strip()
            return True
        except Exception:
            return False

    def as_dict(self):
        return dict(self._data)


def _create_instance_ids(count, result_list):
    for _ in range(count):
        cfg = GlobalConfig()
        result_list.append(id(cfg))


if __name__ == "__main__":
    config_a = GlobalConfig({"mode": "production"})
    config_a.set_value("timeout", 30)

    config_b = GlobalConfig()
    print("config_a id:", id(config_a))
    print("config_b id:", id(config_b))
    print("timeout from b:", config_b.get_value("timeout"))

    thread_count = 10
    instances_per_thread = 5
    threads = []
    collected_ids = []
    for _ in range(thread_count):
        t = threading.Thread(target=_create_instance_ids, args=(instances_per_thread, collected_ids))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    unique_ids = set(collected_ids + [id(config_a), id(config_b)])
    if len(unique_ids) != 1:
        raise RuntimeError("Multiple configuration objects were created")
    print("All threads received the same object id:", unique_ids.pop())
    success = config_a.load_from_file("nonexistent.conf")
    print("Loading nonexistent file returned:", success)
    print("Current config:", config_a.as_dict())