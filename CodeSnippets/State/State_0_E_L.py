class Machine(object):
    def __init__(self, state_name):
        self._state = None
        self.set_state(state_name)
    
    def set_state(self, state_name):
        if state_name == "A":
            self._state = StateA()
        elif state_name == "B":
            self._state = StateB()
        else:
            raise ValueError("Invalid state name")
    
    def get_state(self):
        return self._state
    
class StateA(object):
    def handle_event(self, event):
        if event == "on":
            print("State A on")
        elif event == "off":
            print("State A off")
        else:
            raise ValueError("Invalid event")
    
class StateB(object):
    def handle_event(self, event):
        if event == "on":
            print("State B on")
        elif event == "off":
            print("State B off")
        else:
            raise ValueError("Invalid event")
    
# Example usage
machine = Machine("A")
machine.handle_event("on") # Outputs: State A on
machine.set_state("B")
machine.handle_event("off") # Outputs: State B off