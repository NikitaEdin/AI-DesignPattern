import threading
import json
import concurrent.futures

class UniqueInstanceMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with UniqueInstanceMeta._lock:
            if cls not in UniqueInstanceMeta._instances:
                instance = super().__call__(*args, **kwargs)
                UniqueInstanceMeta._instances[cls] = instance
            return UniqueInstanceMeta._instances[cls]

class AppConfigManager(metaclass=UniqueInstanceMeta):
    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._settings = {}
        self._initialized = True
        self._internal_lock = threading.RLock()

    def set_setting(self, key, value):
        with self._internal_lock:
            if not isinstance(key, str):
                raise TypeError("Key must be a string")
            self._settings[key] = value

    def get_setting(self, key, default=None):
        with self._internal_lock:
            return self._settings.get(key, default)

    def load_from_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Configuration file must contain a JSON object")
            with self._internal_lock:
                self._settings.update(data)
        except Exception as exc:
            raise RuntimeError(f"Failed to load configuration: {exc}") from exc

    def all_settings(self):
        with self._internal_lock:
            return dict(self._settings)

if __name__ == "__main__":
    def create_and_report():
        inst = AppConfigManager()
        inst.set_setting("created_by", threading.current_thread().name)
        return id(inst)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        ids = list(executor.map(lambda _: create_and_report(), range(8)))

    print("All IDs equal:", all(i == ids[0] for i in ids))

    a = AppConfigManager()
    b = AppConfigManager()
    a.set_setting("mode", "active")
    print("Shared value:", b.get_setting("mode"))
    print("Same object:", a is b)
    try:
        # Demonstrate error handling for a non-existent file
        a.load_from_file("nonexistent_config.json")
    except RuntimeError as e:
        print("Load error caught:", str(e))