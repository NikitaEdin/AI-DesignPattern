class Proxy:
    def __init__(self, real_object):
        self._real_object = real_object
        
    def __getattr__(self, attr):
        return getattr(self._real_object, attr)
    
    def __setattr__(self, attr, value):
        setattr(self._real_object, attr, value)
        
class RealObject:
    def __init__(self, name):
        self.name = name
        
    def get_name(self):
        return self.name
        
if __name__ == "__main__":
    real_object = RealObject("John")
    proxy = Proxy(real_object)
    
    print(proxy.get_name())  # Output: John
    
    proxy.name = "Jane"
    print(real_object.name)  # Output: Jane