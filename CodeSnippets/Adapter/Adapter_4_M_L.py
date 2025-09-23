class Target:
    def __init__(self):
        self.name = "Target"

    def method1(self):
        print("Target method1")

    def method2(self):
        print("Target method2")


class Adapter:
    def __init__(self, target):
        self.target = target

    def method3(self):
        print("Adapter method3")

    def method4(self):
        print("Adapter method4")


def main():
    # Create an instance of the Target class
    target_instance = Target()

    # Use the Adapter to call methods on the Target object
    adapter_instance = Adapter(target_instance)
    adapter_instance.method3()
    adapter_instance.method4()

if __name__ == "__main__":
    main()