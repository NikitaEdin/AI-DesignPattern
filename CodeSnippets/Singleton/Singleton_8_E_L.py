class Singleton:
    def __init__(self):
        self._instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

# Usage example in a main section
if __name__ == "__main__":
    # Create two instances of the Singleton class
    s1 = Singleton.get_instance()
    s2 = Singleton.get_instance()

    # Both instances are the same object
    assert s1 is s2

    # Modify the state of one instance
    s1.data = 42

    # The other instance's state also changes
    assert s2.data == 42