import sys

class Task:
    def execute(self):
        pass

    def undo(self):
        pass

class LightOn(Task):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.switch(True)
    
    def undo(self):
        self.light.switch(False)

class LightOff(Task):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.switch(False)
    
    def undo(self):
        self.light.switch(True)

class Light:
    def __init__(self):
        self.state = False
    
    def switch(self, state):
        self.state = state
        print(f"Light {'ON' if state else 'OFF'}")

class Remote:
    def __init__(self):
        self.history = []
    
    def press(self, task):
        try:
            task.execute()
            self.history.append(task)
        except Exception:
            print("Error executing task", file=sys.stderr)
    
    def back(self):
        if self.history:
            self.history.pop().undo()

if __name__ == "__main__":
    light = Light()
    remote = Remote()
    remote.press(LightOn(light))
    remote.press(LightOff(light))
    remote.back()