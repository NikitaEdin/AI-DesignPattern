class Light:
    def on(self): print("Light on")
    def off(self): print("Light off")

class Fan:
    def on(self): print("Fan on")
    def off(self): print("Fan off")

class Speaker:
    def on(self): print("Speaker on")
    def off(self): print("Speaker off")

class RoomControl:
    def __init__(self):
        self.light = Light()
        self.fan = Fan()
        self.speaker = Speaker()
    def start(self):
        self.light.on()
        self.fan.on()
        self.speaker.on()
    def stop(self):
        self.light.off()
        self.fan.off()
        self.speaker.off()

if __name__ == "__main__":
    control = RoomControl()
    control.start()
    control.stop()