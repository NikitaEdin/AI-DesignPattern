class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.value = 42


if __name__ == "__main__":
    a = AppConfig()
    b = AppConfig()
    print(a is b)
    print(a.value)
    b.value = 100
    print(a.value)