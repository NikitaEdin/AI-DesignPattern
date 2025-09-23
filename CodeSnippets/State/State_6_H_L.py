class Machine:
    def __init__(self, state):
        self.state = state
    
    def process(self, input):
        return self.state.process(input)
    
    def transition(self, new_state):
        self.state = new_state

class State:
    def __init__(self, name):
        self.name = name
    
    def process(self, input):
        return None

class StateA(State):
    def process(self, input):
        if input == "a":
            return "Processed in A"
        else:
            return None

class StateB(State):
    def process(self, input):
        if input == "b":
            return "Processed in B"
        else:
            return None

machine = Machine(StateA("A"))
print(machine.process("a"))  # Output: Processed in A
print(machine.process("b"))  # Output: None
machine.transition(StateB("B"))
print(machine.process("b"))  # Output: Processed in B