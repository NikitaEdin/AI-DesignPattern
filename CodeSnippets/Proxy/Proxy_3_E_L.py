class RealObject:
    def do_something(self):
        print("I am a real object!")

class ProxyObject:
    def __init__(self, real_object):
        self.real_object = real_object

    def do_something(self):
        self.real_object.do_something()