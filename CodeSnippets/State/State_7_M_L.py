# State design pattern implementation with context object
class Machine:
    def __init__(self):
        self.state = None

    def update(self, event):
        if self.state is not None:
            # Handle event in current state
            self.state.handle(event)

# States
class StateA:
    def handle(self, event):
        print("Handling event in State A")

class StateB:
    def handle(self, event):
        print("Handling event in State B")

# Context object
machine = Machine()

# Usage example
machine.update("event1")  # Output: Handling event in State A
machine.update("event2")  # Output: Handling event in State B