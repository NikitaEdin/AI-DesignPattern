class Target:
    def request(self):
        print("Target method called")

class Adapter:
    def __init__(self, target):
        self.target = target

    def request(self):
        self.target.request()

if __name__ == "__main__":
    target = Target()
    adapter = Adapter(target)
    adapter.request()