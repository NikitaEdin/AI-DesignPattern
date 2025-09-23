class Target:
    def request(self):
        print("Target class called")

class Adapter:
    def __init__(self, target):
        self._target = target

    def request(self):
        self._target.request()
        print("Adapter class called")

if __name__ == "__main__":
    t = Target()
    a = Adapter(t)
    a.request()