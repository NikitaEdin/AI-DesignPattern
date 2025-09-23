# Adapter pattern implementation in Python

class Target:
    def request(self):
        print("Target.request()")

class Adaptee:
    def specific_request(self):
        print("Adaptee.specific_request()")

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        self.adaptee.specific_request()

# Usage example
target = Target()
target.request()

adapter = Adapter(Adaptee())
adapter.request()