class Target():
    def specific_request(self):
        return "specific_request"

class Adaptee():
    def request(self):
        return "request"

class Adapter():
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def specific_request(self):
        return self.adaptee.request() + "_adapted"

def main():
    target = Target()
    adapter = Adapter(Adaptee())
    print(target.specific_request()) # prints "specific_request_adapted"

if __name__ == "__main__":
    main()