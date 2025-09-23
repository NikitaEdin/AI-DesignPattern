class Target:
    def request(self):
        print("Target::request()")

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        self.adaptee.specific_request()

class Adaptee:
    def specific_request(self):
        print("Adaptee::specific_request()")

def main():
    target = Target()
    adapter = Adapter(target)
    adapter.request()
    
if __name__ == "__main__":
    main()