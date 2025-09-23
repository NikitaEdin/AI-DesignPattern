class MySingleton:
    """
    A simple Singleton implementation.
    """
    __instance = None

    def __init__(self):
        if MySingleton.__instance is not None:
            raise RuntimeError("Cannot create a new instance of a singleton class")
        else:
            MySingleton.__instance = self

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance.
        """
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

def main():
    # Create a new instance of the singleton class
    instance1 = MySingleton.get_instance()

    # Get another reference to the same instance
    instance2 = MySingleton.get_instance()

    # Ensure that both references point to the same object
    assert id(instance1) == id(instance2)

if __name__ == "__main__":
    main()