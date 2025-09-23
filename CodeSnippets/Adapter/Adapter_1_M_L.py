class Target:
    def request(self):
        print("Target Request")

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return self.adaptee.specific_request()

class Adaptee:
    def specific_request(self):
        print("Adaptee Request")

# Usage example
target = Target()
adapter = Adapter(Adaptee())
target.request()  # Output: Target Request
adapter.request()  # Output: Adaptee Request