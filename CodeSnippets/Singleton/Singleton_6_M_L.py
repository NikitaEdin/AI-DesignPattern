class MySingleton:
    def __init__(self):
        self._instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def some_method(self):
        # do something useful
        pass

if __name__ == "__main__":
    singleton1 = MySingleton.get_instance()
    singleton2 = MySingleton.get_instance()
    print(singleton1 is singleton2)  # True