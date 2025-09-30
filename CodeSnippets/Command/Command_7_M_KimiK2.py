import time
from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def execute(self): ...

    @abstractmethod
    def undo(self): ...

class LightOn(Task):
    def __init__(self, device): self.device = device
    def execute(self): self.device.power(True)
    def undo(self): self.device.power(False)

class LightOff(Task):
    def __init__(self, device): self.device = device
    def execute(self): self.device.power(False)
    def undo(self): self.device.power(True)

class SpeakerPlay(Task):
    def __init__(self, device, track): self.device, self.track = device, track
    def execute(self): self.device.play(self.track)
    def undo(self): self.device.stop()

class Macro(Task):
    def __init__(self, steps): self.steps = steps
    def execute(self):
        for step in self.steps: step.execute()
    def undo(self):
        for step in reversed(self.steps): step.undo()

class Remote:
    def __init__(self): self.history = []
    def submit(self, task):
        try:
            task.execute()
            self.history.append(task)
        except Exception as e:
            print("error:", e)
    def rollback(self):
        if self.history:
            self.history.pop().undo()

class Light:
    def __init__(self, name): self.name, self.state = name, False
    def power(self, on): self.state = on; print(f"{self.name} {'on' if on else 'off'}")

class Speaker:
    def __init__(self, name): self.name, self.track = name, None
    def play(self, track): self.track = track; print(f"{self.name} playing {track}")
    def stop(self): print(f"{self.name} stopped"); self.track = None

if __name__ == "__main__":
    living_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    speaker = Speaker("Soundbar")
    remote = Remote()
    movie_night = Macro([LightOff(living_light), LightOff(bedroom_light), SpeakerPlay(speaker, "chill")])
    remote.submit(movie_night)
    remote.rollback()