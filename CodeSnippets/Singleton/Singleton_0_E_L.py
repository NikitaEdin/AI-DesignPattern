class Singleton:
    """
    A simple implementation of the singleton design pattern in Python.
    """

    __instance = None

    def __init__(self):
        if not isinstance(Singleton.__instance, Singleton):
            Singleton.__instance = self

    @classmethod
    def get_instance(cls):
        if not isinstance(Singleton.__instance, Singleton):
            return Singleton()
        else:
            return Singleton.__instance

if __name__ == "__main__":
    # Usage example
    s1 = Singleton.get_instance()
    print("s1:", s1)
    s2 = Singleton.get_instance()
    print("s2:", s2)
    if s1 is s2:
        print("s1 and s2 are the same object")
    else:
        print("s1 and s2 are not the same object")