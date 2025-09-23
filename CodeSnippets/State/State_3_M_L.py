# A simple example of the State design pattern in Python

class CoffeeMachine:
    def __init__(self):
        self.state = None

    def start(self):
        self.state = StartState(self)
        self.state.start()

    def stop(self):
        self.state.stop()

class State:
    def __init__(self, coffee_machine):
        self.coffee_machine = coffee_machine

    def start(self):
        raise NotImplementedError("Start method not implemented")

    def stop(self):
        raise NotImplementedError("Stop method not implemented")

class StartState(State):
    def __init__(self, coffee_machine):
        super().__init__(coffee_machine)

    def start(self):
        print("Starting the coffee machine...")

    def stop(self):
        self.coffee_machine.state = StopState(self.coffee_machine)
        self.coffee_machine.stop()

class StopState(State):
    def __init__(self, coffee_machine):
        super().__init__(coffee_machine)

    def start(self):
        print("Coffee machine is already stopped")

    def stop(self):
        print("Stopping the coffee machine...")

if __name__ == "__main__":
    coffee_machine = CoffeeMachine()
    coffee_machine.start()
    coffee_machine.stop()