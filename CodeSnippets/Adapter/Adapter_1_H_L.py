class Target:
    def __init__(self):
        self.name = "Target"

    def request(self):
        print("Requesting a service from the target")

class Adapter:
    def __init__(self, target):
        self.target = target

    def request(self):
        print("Received a request from the adapter")
        self.target.request()

def main():
    target = Target()
    adapter = Adapter(target)
    adapter.request()

if __name__ == "__main__":
    main()