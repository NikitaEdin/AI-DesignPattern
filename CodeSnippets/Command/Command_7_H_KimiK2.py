import threading
import time
from abc import ABC, abstractmethod
from typing import List, Optional

class Action(ABC):
    @abstractmethod
    def trigger(self): pass
    
    @abstractmethod
    def revoke(self): pass

class Light:
    def __init__(self): self._state = False
    def turn_on(self): self._state = True
    def turn_off(self): self._state = False
    def get_state(self): return self._state

class Volume:
    def __init__(self): self._level = 50
    def set_level(self, level): self._level = max(0, min(100, level))
    def get_level(self): return self._level

class LightOnAction(Action):
    def __init__(self, light: Light):
        self._light = light
        self._prev_state = None
    
    def trigger(self):
        self._prev_state = self._light.get_state()
        self._light.turn_on()
    
    def revoke(self):
        if self._prev_state is not None:
            if not self._prev_state:
                self._light.turn_off()

class LightOffAction(Action):
    def __init__(self, light: Light):
        self._light = light
        self._prev_state = None
    
    def trigger(self):
        self._prev_state = self._light.get_state()
        self._light.turn_off()
    
    def revoke(self):
        if self._prev_state is not None:
            if self._prev_state:
                self._light.turn_on()

class VolumeChangeAction(Action):
    def __init__(self, volume: Volume, target: int):
        self._volume = volume
        self._target = target
        self._prev_level = None
    
    def trigger(self):
        self._prev_level = self._volume.get_level()
        self._volume.set_level(self._target)
    
    def revoke(self):
        if self._prev_level is not None:
            self._volume.set_level(self._prev_level)

class TaskRunner:
    def __init__(self):
        self._queue: List[Action] = []
        self._history: List[Action] = []
        self._lock = threading.Lock()
    
    def schedule(self, action: Action):
        with self._lock:
            self._queue.append(action)
    
    def process(self):
        with self._lock:
            while self._queue:
                action = self._queue.pop(0)
                action.trigger()
                self._history.append(action)
    
    def undo_last(self, count: int = 1):
        with self._lock:
            for _ in range(min(count, len(self._history))):
                action = self._history.pop()
                action.revoke()

if __name__ == "__main__":
    light = Light()
    volume = Volume()
    
    runner = TaskRunner()
    
    runner.schedule(LightOnAction(light))
    runner.schedule(VolumeChangeAction(volume, 75))
    runner.schedule(LightOffAction(light))
    
    runner.process()
    
    print(f"Light state: {light.get_state()}")
    print(f"Volume level: {volume.get_level()}")
    
    runner.undo_last(2)
    
    print(f"After undo - Light state: {light.get_state()}")
    print(f"After undo - Volume level: {volume.get_level()}")