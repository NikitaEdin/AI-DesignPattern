class FSM(object):
    """A finite state machine"""
    
    def __init__(self, states):
        self.states = states
        self.current_state = None
    
    def add_transition(self, trigger, source, dest):
        self.transitions[(trigger, source)] = dest
    
    def process(self, event):
        if self.current_state is None:
            return
        
        try:
            next_state = self.transitions[(event, self.current_state)]
            self.current_state = next_state
        except KeyError:
            print("Invalid transition.")
    
    def get_current_state(self):
        return self.current_state
    
if __name__ == "__main__":
    # Example usage
    fsm = FSM(["A", "B", "C"])
    fsm.add_transition("event1", "A", "B")
    fsm.add_transition("event2", "B", "C")
    fsm.add_transition("event3", "C", "A")
    
    print(fsm.get_current_state())  # Output: A
    
    fsm.process("event1")
    print(fsm.get_current_state())  # Output: B
    
    fsm.process("event2")
    print(fsm.get_current_state())  # Output: C
    
    fsm.process("event3")
    print(fsm.get_current_state())  # Output: A