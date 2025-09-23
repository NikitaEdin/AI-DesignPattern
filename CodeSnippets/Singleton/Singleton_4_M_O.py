import threading

class UniqueInstanceMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with UniqueInstanceMeta._lock:
            if cls not in UniqueInstanceMeta._instances:
                UniqueInstanceMeta._instances[cls] = super().__call__(*args, **kwargs)
            return UniqueInstanceMeta._instances[cls]

class AppConfig(metaclass=UniqueInstanceMeta):
    def __init__(self, defaults=None):
        if getattr(self, "_initialized", False):
            return
        self._config = dict(defaults) if defaults else {}
        self._lock = threading.RLock()
        self._initialized = True

    def set_value(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Configuration keys must be strings")
        with self._lock:
            self._config[key] = value

    def get_value(self, key, default=None):
        with self._lock:
            return self._config.get(key, default)

    def as_dict(self):
        with self._lock:
            return dict(self._config)

def _worker(name, key, value):
    cfg = AppConfig()
    cfg.set_value(key, value)
    print(f"Worker {name}: set {key}={value}; instance id={id(cfg)}")

if __name__ == "__main__":
    config_a = AppConfig({"version": "1.0"})
    config_b = AppConfig()
    print("Same instance:", config_a is config_b)
    print("Initial version:", config_b.get_value("version"))

    config_b.set_value("mode", "production")
    print("Mode from A:", config_a.get_value("mode"))

    threads = []
    for i in range(3):
        t = threading.Thread(target=_worker, args=(i, f"key{i}", f"value{i}"))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print("Final config:", config_a.as_dict())

    try:
        config_a.set_value(123, "bad")
    except Exception as exc:
        print("Error caught:", type(exc).__name__, exc)