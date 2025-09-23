class Target:
    def request(self):
        print("Target method called")

class Adapter:
    def __init__(self, target):
        self.target = target

    def request_1(self):
        self.target.request()

    def request_2(self):
        print("Adapter method called")

def main():
    target = Target()
    adapter = Adapter(target)
    adapter.request_1()
    adapter.request_2()

if __name__ == "__main__":
    main()