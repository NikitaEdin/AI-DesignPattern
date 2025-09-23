class GlobalConfig:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
        return cls._instance
    def __init__(self, value=None):
        if not hasattr(self, "_initialized"):
            self.value = value
            self._initialized = True
    def set_value(self, v):
        self.value = v
    def get_value(self):
        return self.value

if __name__ == "__main__":
    a = GlobalConfig("first")
    b = GlobalConfig("second")
    print(a is b, a.get_value(), b.get_value())
    b.set_value("updated")
    print(a.get_value())