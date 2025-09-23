class RealObject:
    def do_something(self):
        print("Real object doing something")

class Proxy:
    def __init__(self, real_object):
        self.real_object = real_object

    def do_something(self):
        self.real_object.do_something()

if __name__ == "__main__":
    # Create a proxy object for the real object
    real_object = RealObject()
    proxy = Proxy(real_object)

    # Use the proxy object to call the do_something method
    proxy.do_something()