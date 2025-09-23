class Target(object):
    def request(self):
        return "Target method"

class Adapter(object):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return "Adapter method: " + self.adaptee.specific_request()

class Adaptee(object):
    def specific_request(self):
        return "Adaptee method"

if __name__ == "__main__":
    adaptee = Adaptee()
    adapter = Adapter(adaptee)

    print("Target method:")
    print(adapter.request())

    print("\nAdaptee method:")
    print(adaptee.specific_request())