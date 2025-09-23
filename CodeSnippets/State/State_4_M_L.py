class Machine:
    def __init__(self):
        self.state = "idle"
    
    def start(self):
        self.state = "running"
        print("Machine started")
    
    def stop(self):
        self.state = "idle"
        print("Machine stopped")
    
    def is_idle(self):
        return self.state == "idle"
    
    def is_running(self):
        return self.state == "running"