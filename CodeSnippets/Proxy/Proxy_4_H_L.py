class Proxy:
    def __init__(self, target):
        self.target = target

    def operation(self):
        print("Proxying the operation")
        return self.target.operation()

class Target:
    def operation(self):
        print("Target operation called")
        return "result"

if __name__ == "__main__":
    target = Target()
    proxy = Proxy(target)
    result = proxy.operation()
    print(result)