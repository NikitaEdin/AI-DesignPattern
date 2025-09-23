```
class RealObject():
    def __init__(self):
        print("Real Object Created")
    
    def do_something(self):
        print("Real Object is doing something")

class Proxy():
    def __init__(self, real_object):
        self.real_object = real_object
    
    def do_something(self):
        self.real_object.do_something()
    
if __name__ == "__main__":
    # Create a proxy object
    proxy = Proxy(RealObject())
    
    # Use the proxy object to call the do_something method on the real object
    proxy.do_something()
         ```