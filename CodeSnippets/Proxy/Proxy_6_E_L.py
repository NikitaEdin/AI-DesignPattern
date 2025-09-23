class RealObject:
    def do_something(self):
        print("Real object does something.")

class Proxy:
    def __init__(self, real_object):
        self.real_object = real_object

    def do_something(self):
        self.real_object.do_something()

if __name__ == "__main__":
    # Create a proxy object for a real object
    proxy = Proxy(RealObject())

    # Use the proxy object as if it were the real object
    proxy.do_something()