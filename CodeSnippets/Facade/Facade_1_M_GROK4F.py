class Screen:
    def down(self):
        print("Screen is down")

    def up(self):
        print("Screen is up")

class Projector:
    def __init__(self, screen):
        self.screen = screen
        self.on = False

    def on(self):
        self.on = True
        print("Projector is on")

    def off(self):
        self.on = False
        print("Projector is off")

    def set_input(self, source):
        print(f"Projector setting input to {source}")

class Amplifier:
    def __init__(self):
        self.on = False
        self.volume = 0

    def on(self):
        self.on = True
        print("Amplifier is on")

    def off(self):
        self.on = False
        print("Amplifier is off")

    def set_volume(self, volume):
        self.volume = volume
        print(f"Setting volume to {volume}")

class StreamingPlayer:
    def __init__(self):
        self.on = False

    def on(self):
        self.on = True
        print("Streaming player is on")

    def off(self):
        self.on = False
        print("Streaming player is off")

    def play(self, movie):
        print(f"Playing {movie}")

class HomeTheaterSystem:
    def __init__(self, projector, screen, amplifier, player):
        self.projector = projector
        self.screen = screen
        self.amplifier = amplifier
        self.player = player

    def watch_movie(self, movie):
        try:
            self.screen.down()
            self.projector.on()
            self.projector.set_input("HDMI")
            self.amplifier.on()
            self.amplifier.set_volume(5)
            self.player.on()
            self.player.play(movie)
            print("Enjoy the show!")
        except Exception as e:
            print(f"Error during movie start: {e}")

    def end_movie(self):
        try:
            self.player.off()
            self.amplifier.off()
            self.projector.off()
            self.screen.up()
            print("Shutdown complete.")
        except Exception as e:
            print(f"Error during shutdown: {e}")

if __name__ == "__main__":
    screen = Screen()
    projector = Projector(screen)
    amplifier = Amplifier()
    player = StreamingPlayer()
    theater = HomeTheaterSystem(projector, screen, amplifier, player)
    theater.watch_movie("Avengers")
    theater.end_movie()