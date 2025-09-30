class TrafficLight:
    def __init__(self):
        self.mode = RedMode()
    def change(self):
        self.mode.switch(self)
    def view(self):
        return self.mode.message()

class RedMode:
    def switch(self, ctx):
        ctx.mode = GreenMode()
    def message(self):
        return "Red light - Stop"

class GreenMode:
    def switch(self, ctx):
        ctx.mode = YellowMode()
    def message(self):
        return "Green light - Go"

class YellowMode:
    def switch(self, ctx):
        ctx.mode = RedMode()
    def message(self):
        return "Yellow light - Caution"

if __name__ == "__main__":
    light = TrafficLight()
    for _ in range(4):
        print(light.view())
        light.change()