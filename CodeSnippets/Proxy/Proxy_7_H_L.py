class RealObject:
    def __init__(self, name):
        self.name = name
    
    def do_something(self):
        print("RealObject does something.")

class Proxy:
    def __init__(self, real_object):
        self.real_object = real_object
    
    def do_something(self):
        # Perform some pre-processing
        self.real_object.do_something()
        # Perform some post-processing

if __name__ == "__main__":
    real_object = RealObject("Bob")
    proxy = Proxy(real_object)
    proxy.do_something()