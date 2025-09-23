class AppConfig:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    def __init__(self, start_value=None):
        if self._initialized:
            return
        self.value = start_value
        self._initialized = True
    def set_value(self, v):
        self.value = v
    def get_value(self):
        return self.value

if __name__ == "__main__":
    a = AppConfig(10)
    b = AppConfig(20)
    print(a is b)
    print(a.get_value(), b.get_value())
    b.set_value(30)
    print(a.get_value(), b.get_value())
    print(id(a), id(b))