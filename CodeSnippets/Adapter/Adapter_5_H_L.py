class Target:
    def request(self):
        print("Target method called")

class Adapter:
    def __init__(self, target):
        self.target = target

    def request(self):
        print("Adapter method called")
        self.target.request()

if __name__ == "__main__":
    t = Target()
    a = Adapter(t)
    a.request()