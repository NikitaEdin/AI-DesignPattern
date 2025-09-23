class RealObject:
    def do_something(self):
        print("Real Object")

class Proxy:
    def __init__(self, real_object):
        self.real_object = real_object

    def do_something(self):
        print("Proxy")
        self.real_object.do_something()

if __name__ == "__main__":
    real_object = RealObject()
    proxy = Proxy(real_object)
    proxy.do_something()