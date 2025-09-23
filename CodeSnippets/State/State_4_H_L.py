import time

class State:
    """A state represents a specific condition of an object."""

    def __init__(self, name):
        self.name = name

    def enter(self):
        print(f"Entering {self.name} state")

    def exit(self):
        print(f"Exiting {self.name} state")

class Context:
    """The context maintains a reference to the current state object."""

    def __init__(self, initial_state=None):
        self._current = initial_state

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        if not isinstance(value, State):
            raise ValueError("Current state must be an instance of State")
        self._current = value

class ConcreteStateA(State):
    def handle(self, context):
        print("Handling event A in state A")
        time.sleep(1)
        context.current = ConcreteStateB()

class ConcreteStateB(State):
    def handle(self, context):
        print("Handling event B in state B")
        time.sleep(1)
        context.current = ConcreteStateA()

if __name__ == "__main__":
    # Create an instance of the context class with initial state A
    context = Context(initial_state=ConcreteStateA())

    # Simulate events and observe the behavior of the context
    for _ in range(5):
        event = input("Enter event (A or B): ")
        if event == "A":
            context.current.handle(context)
        elif event == "B":
            context.current.handle(context)
        else:
            print("Invalid event")

    # Print the final state of the context
    print(f"Final state: {context.current.name}")