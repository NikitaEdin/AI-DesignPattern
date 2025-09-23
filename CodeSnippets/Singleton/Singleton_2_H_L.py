class Singleton:
    """
    A class that implements the Singleton design pattern.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

class ExampleUsage:
    """
    A class that demonstrates the usage of the Singleton pattern.
    """

    def main(self):
        # Create a new instance of the singleton
        s1 = Singleton()

        # Get another reference to the same instance
        s2 = Singleton()

        # Check if both references are the same object
        print(s1 is s2)  # Output: True

if __name__ == "__main__":
    ExampleUsage().main()