class Target:
    def request(self):
        print("Target class is requesting a service.")

class Adapter:
    def __init__(self, adapter_object):
        self.adapter_object = adapter_object

    def request(self):
        print("Adapter class is requesting a service.")
        self.adapter_object.request()

class Adaptee:
    def request(self):
        print("Adaptee class is requesting a service.")

# Usage example
target = Target()
adaptee = Adaptee()
adapter = Adapter(adaptee)
target.request()