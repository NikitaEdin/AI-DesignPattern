class Singleton:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        pass

if __name__ == "__main__":
    s1 = Singleton.instance()
    s2 = Singleton.instance()
    print(id(s1), id(s2)) # Should be the same object