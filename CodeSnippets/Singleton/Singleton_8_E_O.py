class GlobalResource:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        if getattr(self, "_initialized", False):
            return
        self.value = value
        self._initialized = True

if __name__ == "__main__":
    a = GlobalResource(10)
    b = GlobalResource(20)
    print(a is b)
    print(a.value, b.value)