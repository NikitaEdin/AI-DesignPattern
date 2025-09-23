from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class LightToggle(Action):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class VolumeAdjust(Action):
    def __init__(self, stereo, volume):
        self.stereo = stereo
        self.volume = volume
        self.previous_volume = 0
    
    def execute(self):
        self.previous_volume = self.stereo.volume
        self.stereo.set_volume(self.volume)
    
    def undo(self):
        self.stereo.set_volume(self.previous_volume)

class Light:
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print("Light is on")
    
    def turn_off(self):
        self.is_on = False
        print("Light is off")

class Stereo:
    def __init__(self):
        self.volume = 0
    
    def set_volume(self, level):
        self.volume = level
        print(f"Volume set to {level}")

class RemoteControl:
    def __init__(self):
        self.history = []
    
    def press_button(self, action):
        try:
            action.execute()
            self.history.append(action)
        except Exception as e:
            print(f"Error executing action: {e}")
    
    def press_undo(self):
        if self.history:
            last_action = self.history.pop()
            last_action.undo()

if __name__ == "__main__":
    light = Light()
    stereo = Stereo()
    remote = RemoteControl()
    
    light_action = LightToggle(light)
    volume_action = VolumeAdjust(stereo, 5)
    
    remote.press_button(light_action)
    remote.press_button(volume_action)
    remote.press_undo()
    remote.press_undo()