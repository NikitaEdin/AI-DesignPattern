class LightMode:
    def switch(self, bulb): raise NotImplementedError
    def status(self): raise NotImplementedError

class Brightness(LightMode):
    def switch(self, bulb): bulb.mode = Dimmed()
    def status(self): return "Bright"

class Dimmed(LightMode):
    def switch(self, bulb): bulb.mode = Off()
    def status(self): return "Dimmed"

class Off(LightMode):
    def switch(self, bulb): bulb.mode = Brightness()
    def status(self): return "Off"

class Bulb:
    def __init__(self): self.mode = Off()
    def flip(self): self.mode.switch(self)
    def info(self): return self.mode.status()

if __name__ == "__main__":
    lamp = Bulb()
    for _ in range(4):
        print(lamp.info())
        lamp.flip()