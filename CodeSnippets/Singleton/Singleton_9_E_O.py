class GlobalConfig:
    _instance = None
    def __new__(cls, *a, **k):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_done = False
        return cls._instance
    def __init__(self):
        if self._init_done:
            return
        self.values = {}
        self._init_done = True
    def set(self, k, v):
        self.values[k] = v
    def get(self, k, default=None):
        return self.values.get(k, default)

if __name__ == "__main__":
    a = GlobalConfig()
    b = GlobalConfig()
    a.set("mode", "production")
    print(b.get("mode"))
    print(a is b)