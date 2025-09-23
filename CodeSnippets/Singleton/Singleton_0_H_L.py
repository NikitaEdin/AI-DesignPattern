class SingletonClass():
    _instance = None
    
    def __init__(self):
        if self._instance is None:
            self._instance = self
    
    @classmethod
    def get_instance(cls) -> 'SingletonClass':
        return cls._instance
        
    def get_message(self) -> str:
        return "Hello World!"