class Target:
    def request(self):
        print("Target method called")

class Adapter:
    def __init__(self, target):
        self.target = target

    def request_wrapper(self):
        self.target.request()
        print("Adapter method called")

# Usage example
target = Target()
adapter = Adapter(target)
adapter.request_wrapper()