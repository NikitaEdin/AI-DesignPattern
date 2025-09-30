from abc import ABC, abstractmethod

class LightMode(ABC):
    @abstractmethod
    def click(self, context):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

class OffMode(LightMode):
    def click(self, context):
        context.set_mode(LowMode())
    
    def __str__(self):
        return "Off"

class LowMode(LightMode):
    def click(self, context):
        context.set_mode(HighMode())
    
    def __str__(self):
        return "Low"

class HighMode(LightMode):
    def click(self, context):
        context.set_mode(OffMode())
    
    def __str__(self):
        return "High"

class LightControl:
    def __init__(self):
        self._mode = OffMode()
    
    def click(self):
        self._mode.click(self)
    
    def set_mode(self, mode):
        self._mode = mode
    
    def __str__(self):
        return str(self._mode)

if __name__ == "__main__":
    light = LightControl()
    print(light)
    for _ in range(5):
        light.click()
        print(light)