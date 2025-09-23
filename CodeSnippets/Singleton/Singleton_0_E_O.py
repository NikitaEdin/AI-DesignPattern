class GlobalResource:
    _shared = None

    def __new__(cls, *args, **kwargs):
        if cls._shared is None:
            cls._shared = super().__new__(cls)
            cls._shared.value = kwargs.get('value', 0)
        return cls._shared

    def set_value(self, v):
        self.value = v

    def get_value(self):
        return self.value

if __name__ == "__main__":
    a = GlobalResource(value=10)
    b = GlobalResource()
    print(a.get_value(), b.get_value())
    b.set_value(20)
    print(a.get_value(), b.get_value())
    print(a is b)