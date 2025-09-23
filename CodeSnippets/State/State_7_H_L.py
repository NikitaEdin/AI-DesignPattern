class Machine:
    def __init__(self, state):
        self.state = state
    
    def change_state(self, new_state):
        if self.state.is_valid_transition(new_state):
            self.state = new_state
            return True
        else:
            return False
    
    def current_state(self):
        return self.state
    
class State:
    def __init__(self, name):
        self.name = name
    
    def is_valid_transition(self, new_state):
        return True
    
class RunningState(State):
    def is_valid_transition(self, new_state):
        return new_state == "Stopped"
    
class StoppedState(State):
    def is_valid_transition(self, new_state):
        return new_state == "Running"
    
machine = Machine("Running")
print(machine.current_state()) # Output: Running
machine.change_state("Stopped")
print(machine.current_state()) # Output: Stopped