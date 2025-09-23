class UniqueManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UniqueManager, cls).__new__(cls)
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
    a = UniqueManager(10)
    b = UniqueManager(20)
    print(a is b)
    print(a.get_value(), b.get_value())
    b.set_value(30)
    print(a.get_value())