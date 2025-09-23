class Amplifier:
    def on(self):
        print("Amplifier is on")

    def set_dvd(self, dvd):
        print(f"Amplifier setting DVD player to DVD {dvd}")

    def set_volume(self, level):
        print(f"Amplifier setting volume to {level}")

class DvdPlayer:
    def on(self):
        print("DVD Player is on")

    def play(self, movie):
        print(f"DVD Player playing {movie}")

class Projector:
    def on(self):
        print("Projector is on")

    def set_input(self, input_source):
        print(f"Projector setting input to {input_source}")

    def wide_screen_mode(self):
        print("Projector in widescreen mode")

class Screen:
    def down(self):
        print("Theater screen is down")

    def up(self):
        print("Theater screen is up")

class HomeTheater:
    def __init__(self, amp, dvd, projector, screen):
        self.amp = amp
        self.dvd = dvd
        self.projector = projector
        self.screen = screen

    def watch_movie(self, movie):
        try:
            self.screen.down()
            self.projector.on()
            self.projector.set_input("DVD")
            self.projector.wide_screen_mode()
            self.amp.on()
            self.amp.set_dvd(self.dvd)
            self.amp.set_volume(5)
            self.dvd.on()
            self.dvd.play(movie)
            print("Enjoy the movie!")
        except AttributeError as e:
            print(f"Error setting up theater: {e}")

    def end_movie(self):
        try:
            self.dvd.off() if hasattr(self.dvd, 'off') else None
            self.amp.off() if hasattr(self.amp, 'off') else None
            self.projector.off() if hasattr(self.projector, 'off') else None
            self.screen.up()
            print("Movie ended.")
        except AttributeError as e:
            print(f"Error shutting down: {e}")

if __name__ == "__main__":
    amp = Amplifier()
    dvd = DvdPlayer()
    projector = Projector()
    screen = Screen()
    theater = HomeTheater(amp, dvd, projector, screen)
    theater.watch_movie("Inception")
    theater.end_movie()