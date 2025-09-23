# Adapter Design Pattern - Python Implementation

class Target:
    def request(self):
        print("Target Request")

class Adaptee:
    def specific_request(self):
        print("Adaptee Specific Request")

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        self.adaptee.specific_request()

# Usage Example
target = Target()
adaptee = Adaptee()
adapter = Adapter(adaptee)
target.request() # Output: Target Request
adapter.request() # Output: Adaptee Specific Request