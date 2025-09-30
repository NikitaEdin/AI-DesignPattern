class Lights:
    def dim(self):
        pass

class Projector:
    def on(self):
        pass

class System:
    def start(self):
        pass

class MediaCenter:
    def __init__(self):
        self.lights = Lights()
        self.projector = Projector()
        self.system = System()
    def start(self):
        self.lights.dim()
        self.projector.on()
        self.system.start()
    def end(self):
        pass

if __name__ == "__main__":
    center = MediaCenter()
    center.start()
    center.end()