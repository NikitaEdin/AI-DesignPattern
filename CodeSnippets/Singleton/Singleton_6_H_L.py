class MySingleton:
    """A simple Singleton implementation"""
    
    __instance = None
    
    def __init__(self):
        """Initialize the instance variable to point to the current object"""
        self.__instance = self
    
    @classmethod
    def get_instance(cls) -> "MySingleton":
        """Return the singleton instance"""
        return cls.__instance
        
if __name__ == "__main__":
    # Create a new instance of MySingleton
    my_singleton = MySingleton()
    
    # Get the singleton instance
    instance1 = MySingleton.get_instance()
    instance2 = MySingleton.get_instance()
    
    print(id(my_singleton))  # Should be the same as id(instance1) and id(instance2)
```
This code defines a class `MySingleton` that implements the Singleton pattern. The class has an `__init__` method that initializes the instance variable to point to the current object, and a `get_instance` classmethod that returns the singleton instance. The main section creates a new instance of `MySingleton`, gets the singleton instance using the `get_instance` method twice, and prints the ids of the three objects to ensure they are the same.