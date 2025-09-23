class Proxy:
    def __init__(self, real_object):
        self._real_object = real_object
    
    def __getattr__(self, name):
        return getattr(self._real_object, name)
    
    def __setattr__(self, name, value):
        setattr(self._real_object, name, value)
    
    def __delattr__(self, name):
        delattr(self._real_object, name)
    
    def __repr__(self):
        return repr(self._real_object)

class RealObject:
    def __init__(self, name):
        self.name = name
    
    def say_hello(self):
        print(f"Hello, my name is {self.name}!")

if __name__ == "__main__":
    # Create a proxy object for the RealObject
    real_object = Proxy(RealObject("Alice"))
    
    # Access the method on the proxy object
    real_object.say_hello()