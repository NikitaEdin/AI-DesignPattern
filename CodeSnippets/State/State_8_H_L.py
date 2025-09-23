class Machine:
    def __init__(self, state):
        self.state = state

    def process(self, input_data):
        self.state.process(input_data)

    def change_state(self, new_state):
        self.state = new_state

class State:
    def process(self, input_data):
        raise NotImplementedError("Method 'process' not implemented")

class InitialState(State):
    def process(self, input_data):
        print("Initial state: {}".format(input_data))

class FinalState(State):
    def process(self, input_data):
        print("Final state: {}".format(input_data))

if __name__ == "__main__":
    machine = Machine(InitialState())
    machine.process("input data")
    machine.change_state(FinalState())
    machine.process("input data")