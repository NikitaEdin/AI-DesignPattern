class Singleton:
    """A singleton class."""
    
    __instance = None
    
    def __init__(self):
        """Initialize a singleton instance."""
        if not self.__instance:
            self.__instance = self
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance."""
        return cls.__instance