class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
        return cls._instance

    def set_value(self, val):
        self.value = val

    def get_value(self):
        return self.value

if __name__ == "__main__":
    obj1 = AppConfig()
    obj1.set_value(10)

    obj2 = AppConfig()
    print(obj2.get_value())