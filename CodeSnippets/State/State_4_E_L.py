```
class Machine:
    def __init__(self):
        self.state = None
    
    def set_state(self, state):
        self.state = state
    
    def get_state(self):
        return self.state
    
    def handle(self, event):
        if self.state:
            self.state.handle(event)
        else:
            print("No current state")
        
class StateA:
    def handle(self, event):
        if event == "start":
            print("Starting A")
        elif event == "stop":
            print("Stopping A")
    
class StateB:
    def handle(self, event):
        if event == "start":
            print("Starting B")
        elif event == "stop":
            print("Stopping B")
        
if __name__ == "__main__":
    machine = Machine()
    machine.set_state(StateA())
    machine.handle("start")
    machine.set_state(StateB())
    machine.handle("stop")
    ```