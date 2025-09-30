import sys
from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def execute(self): pass
    
    @abstractmethod
    def undo(self): pass

class Light:
    def __init__(self, name): self.name = name
    def turn_on(self): print(f"{self.name} light is ON")
    def turn_off(self): print(f"{self.name} light is OFF")

class LightOn(Task):
    def __init__(self, light): self.light = light
    def execute(self): self.light.turn_on()
    def undo(self): self.light.turn_off()

class LightOff(Task):
    def __init__(self, light): self.light = light
    def execute(self): self.light.turn_off()
    def undo(self): self.light.turn_on()

class Remote:
    def __init__(self): self.history = []
    def submit(self, task):
        try:
            task.execute()
            self.history.append(task)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
    def rollback(self):
        if self.history:
            self.history.pop().undo()

if __name__ == "__main__":
    living_room = Light("Living Room")
    kitchen = Light("Kitchen")
    remote = Remote()
    
    remote.submit(LightOn(living_room))
    remote.submit(LightOff(kitchen))
    remote.rollback()
    remote.rollback()