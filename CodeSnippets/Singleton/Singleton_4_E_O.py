class UniqueObject:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
        return cls._instance
    def set_value(self, v):
        self.value = v
    def get_value(self):
        return self.value

if __name__ == "__main__":
    a = UniqueObject()
    b = UniqueObject()
    a.set_value(42)
    print(a is b)
    print(b.get_value())