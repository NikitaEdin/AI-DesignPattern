# Adapter Pattern Implementation

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
if __name__ == "__main__":
    target = Target()
    target.request()

    adaptee = Adaptee()
    adapter = Adapter(adaptee)
    adapter.request()