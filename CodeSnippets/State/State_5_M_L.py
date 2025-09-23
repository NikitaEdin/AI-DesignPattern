import random

class DoorState:
    def __init__(self, state):
        self.state = state

    def toggle_door(self):
        if self.state == 0:
            return DoorState(1)
        else:
            return DoorState(0)

class DoorContext:
    def __init__(self):
        self.state = DoorState(0)

    def toggle_door(self):
        self.state = self.state.toggle_door()

if __name__ == "__main__":
    context = DoorContext()
    print("Initial state:", context.state.state)
    for _ in range(10):
        context.toggle_door()
        print("Current state:", context.state.state)