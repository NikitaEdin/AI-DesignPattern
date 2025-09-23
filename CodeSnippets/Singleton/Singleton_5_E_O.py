class Config:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.values = {}
    def set(self, key, value):
        self.values[key] = value
    def get(self, key, default=None):
        return self.values.get(key, default)

if __name__ == "__main__":
    a = Config()
    b = Config()
    a.set("theme", "dark")
    print(id(a), id(b))
    print(a.get("theme"), b.get("theme"))
    print(a is b)