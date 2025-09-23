class ExampleSingleton:
    """
    An example implementation of the Singleton design pattern in Python.
    This class provides a way to ensure that only one instance of a class is created,
    and it can be accessed from anywhere in the program.
    """
    
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def get_data(self):
        # This method returns some data that is specific to this instance of the class.
        return "Some data"
    
if __name__ == "__main__":
    # Create an instance of the ExampleSingleton class.
    example = ExampleSingleton()
    
    # Access the same instance from another part of the program.
    print(example.get_data())