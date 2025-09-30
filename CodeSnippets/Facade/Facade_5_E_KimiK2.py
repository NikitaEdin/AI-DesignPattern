class Lights:
    def on(self): print("Lights on")
    def off(self): print("Lights off")

class Projector:
    def start(self): print("Projector started")
    def stop(self): print("Projector stopped")

class SoundSystem:
    def play(self): print("Sound playing")
    def pause(self): print("Sound paused")

class HomeTheater:
    def __init__(self):
        self.lights = Lights()
        self.projector = Projector()
        self.sound = SoundSystem()
    def watch_movie(self):
        self.lights.off()
        self.projector.start()
        self.sound.play()
    def end_movie(self):
        self.lights.on()
        self.projector.stop()
        self.sound.pause()

if __name__ == "__main__":
    theater = HomeTheater()
    theater.watch_movie()
    theater.end_movie()