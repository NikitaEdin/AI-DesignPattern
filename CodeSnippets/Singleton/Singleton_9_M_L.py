class SingletonExample(object):
    """Implement the Singleton design pattern."""
    
    _instance = None
    
    @classmethod
    def getInstance(cls, name):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.name = name
        return cls._instance
    
    def __init__(self, name):
        self.name = name
        
if __name__ == "__main__":
    # Create an instance of the class
    instance1 = SingletonExample("John")
    instance2 = SingletonExample("Jane")
    
    # Access the same instance from both variables
    print(instance1 is instance2)  # Should print True
    print(instance1.name)  # Should print "John"
    print(instance2.name)  # Should also print "John"