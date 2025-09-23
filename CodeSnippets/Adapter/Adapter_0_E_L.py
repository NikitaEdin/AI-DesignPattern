class Target:
    def request(self):
        print("Target received a request")

class Adaptee:
    def specific_request(self):
        print("Adaptee received a specific request")

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        self.adaptee.specific_request()

# Usage example
target = Target()
adaptee = Adaptee()
adapter = Adapter(adaptee)
target.request()  # Output: "Adaptee received a specific request"