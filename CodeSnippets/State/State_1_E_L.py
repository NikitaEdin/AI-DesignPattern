class ComputerState:
    def __init__(self):
        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if not isinstance(new_state, ComputerState):
            raise ValueError("New state must be a subclass of ComputerState")
        self._state = new_state

class OnState(ComputerState):
    def turn_on(self):
        print("The computer is now on.")

    def turn_off(self):
        print("The computer is now off.")

class OffState(ComputerState):
    def turn_on(self):
        print("The computer can't be turned on because it's already off.")

    def turn_off(self):
        print("The computer is now off.")

# Usage example
if __name__ == "__main__":
    computer = ComputerState()
    computer.state = OnState()
    computer.state.turn_on()
    computer.state.turn_off()