class Target {
    def request(self):
        print("Target.request()")
}

class Adapter:
    def __init__(self, target):
        self.target = target

    def request(self):
        self.target.handle_request()

class Adaptee {
    def handle_request(self):
        print("Adaptee.handle_request()")
}

def main():
    # Create an instance of the target and adaptee classes
    target = Target()
    adaptee = Adaptee()

    # Wrap the adaptee in an adapter
    adapter = Adapter(adaptee)

    # Call the request method on the target, which will call the handle_request method on the adaptee via the adapter
    target.request()

if __name__ == "__main__":
    main()