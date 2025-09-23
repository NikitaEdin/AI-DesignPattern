class State:
    def __init__(self, initial_state):
        self.current = initial_state
    
    def set_next(self, next_state):
        self.current = next_state
    
    def get_current(self):
        return self.current