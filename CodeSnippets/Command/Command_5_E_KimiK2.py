class Job:
    def do(self): pass

class Lamp:
    def on(self): print("Lamp on")
    def off(self): print("Lamp off")

class LampOn(Job):
    def __init__(self, lamp): self.lamp = lamp
    def do(self): self.lamp.on()

class LampOff(Job):
    def __init__(self, lamp): self.lamp = lamp
    def do(self): self.lamp.off()

class Remote:
    def __init__(self): self.slot = None
    def set_job(self, job): self.slot = job
    def press(self): self.slot.do()

if __name__ == "__main__":
    lamp = Lamp()
    remote = Remote()
    remote.set_job(LampOn(lamp))
    remote.press()
    remote.set_job(LampOff(lamp))
    remote.press()