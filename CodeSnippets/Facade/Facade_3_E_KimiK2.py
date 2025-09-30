class Lights:
    def on(self): print("Lights on")
    def off(self): print("Lights off")

class Projector:
    def start(self): print("Projector start")
    def stop(self): print("Projector stop")

class SoundSystem:
    def volume(self): print("Sound ready")
    def sound_on(self): print("Sound on")

class HomeTheater:
    def __init__(self):
        self.lights = Lights()
        self.projector = Projector()
        self.sound = SoundSystem()
    def watch_movie(self):
        self.lights.off()
        self.projector.start()
        self.sound.volume()
        self.sound.sound_on()

if __name__ == "__main__":
    home = HomeTheater()
    home.watch_movie()