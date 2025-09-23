class RealObject:
    def __init__(self, name):
        self.name = name
    
    def do_something(self):
        print(f"Real object {self.name} doing something")

class ProxyObject:
    def __init__(self, real_object):
        self.real_object = real_object
    
    def do_something(self):
        self.real_object.do_something()

# Usage example
if __name__ == "__main__":
    # Create a proxy object for the real object
    proxy = ProxyObject(RealObject("test"))
    
    # Call the do_something method on the proxy object
    proxy.do_something()