class Target:
    def request(self):
        return "target"

class Adaptee:
    def specific_request(self):
        return "adaptee"

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        result = self.adaptee.specific_request()
        return f"{result} to target"

if __name__ == "__main__":
    adaptee = Adaptee()
    adapter = Adapter(adaptee)
    print(adapter.request())