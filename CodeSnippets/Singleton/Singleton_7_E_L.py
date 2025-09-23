class MyClass:
    """
    A simple Singleton class that allows only one instance of the class to be created.
    """

    __instance = None

    def __init__(self):
        if MyClass.__instance is not None:
            raise Exception("This class can only have one instance")
        else:
            MyClass.__instance = self

    @classmethod
    def get_instance(cls):
        """
        Returns the single instance of the class.
        """
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

if __name__ == "__main__":
    # Create two instances of the class
    obj1 = MyClass()
    obj2 = MyClass()

    # Both objects should be the same instance
    print(obj1 is obj2)  # Should print True