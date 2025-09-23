class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    print(id(s1), id(s2))  # Should print the same ID for both objects