class Singleton:
    """
    A singleton class that allows only one instance to be created.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

if __name__ == "__main__":
    # Create two instances of the singleton class
    s1 = Singleton()
    s2 = Singleton()

    # Check that both instances are the same
    print(id(s1) == id(s2))  # Output: True