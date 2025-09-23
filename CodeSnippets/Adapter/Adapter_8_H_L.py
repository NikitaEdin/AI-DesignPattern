class TargetInterface:
    def request(self):
        pass

class Adapter(TargetInterface):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return self.adaptee.specific_request()

class SpecificRequest:
    def specific_request(self):
        pass

# Usage Example
target = TargetInterface()
adapter = Adapter(SpecificRequest())
target.request()