class Lights:
    def dim(self): print("dimming lights")
    def on(self): print("lights on")

class Projector:
    def start(self): print("projector running")
    def stop(self): print("projector off")

class Player:
    def play(self): print("movie playing")
    def stop(self): print("movie stopped")

class HomeTheater:
    def __init__(self):
        self.lights = Lights()
        self.proj = Projector()
        self.player = Player()
    def watch_movie(self):
        self.lights.dim()
        self.proj.start()
        self.player.play()
    def end_movie(self):
        self.player.stop()
        self.proj.stop()
        self.lights.on()

if __name__ == "__main__":
    ht = HomeTheater()
    ht.watch_movie()
    ht.end_movie()