# A simple Facade pattern implementation in Python

class MyFacade:
    def __init__(self):
        self._component1 = Component1()
        self._component2 = Component2()

    def start(self):
        self._component1.start()
        self._component2.start()

    def stop(self):
        self._component1.stop()
        self._component2.stop()

class Component1:
    def start(self):
        print("Starting component 1...")

    def stop(self):
        print("Stopping component 1...")

class Component2:
    def start(self):
        print("Starting component 2...")

    def stop(self):
        print("Stopping component 2...")

def main():
    facade = MyFacade()
    facade.start()
    # Do some work here
    facade.stop()

if __name__ == "__main__":
    main()