import time

class Light:
    def __init__(self, name):
        self.name = name
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.name} light is ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.name} light is OFF")

class Task:
    def execute(self):
        pass
    
    def undo(self):
        pass

class LightOnTask(Task):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class LightOffTask(Task):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()

class RemoteControl:
    def __init__(self):
        self.history = []
    
    def submit(self, task):
        task.execute()
        self.history.append(task)
    
    def undo_last(self):
        if self.history:
            task = self.history.pop()
            task.undo()

if __name__ == "__main__":
    living_room = Light("Living Room")
    bedroom = Light("Bedroom")
    
    remote = RemoteControl()
    
    remote.submit(LightOnTask(living_room))
    remote.submit(LightOnTask(bedroom))
    remote.submit(LightOffTask(living_room))
    
    remote.undo_last()
    remote.undo_last()