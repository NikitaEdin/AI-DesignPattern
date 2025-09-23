class RealObject:
    def __init__(self, name):
        self.name = name

class ProxyObject:
    def __init__(self, real_object):
        self.real_object = real_object

    def do_something(self):
        print("Proxy object doing something...")
        self.real_object.do_something()

if __name__ == "__main__":
    # Create a real object
    real_object = RealObject("John Doe")

    # Create a proxy object
    proxy_object = ProxyObject(real_object)

    # Use the proxy object to access the real object's methods
    proxy_object.do_something()