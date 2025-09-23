class Amplifier:
    def __init__(self, description):
        self.description = description
        self.volume = 5

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_dvd(self, dvd):
        print(f"{self.description} setting DVD input to {dvd}")

    def set_volume(self, level):
        self.volume = level
        print(f"{self.description} volume set to {level}")

class DvdPlayer:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.current_dvd = None

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def play(self, dvd):
        self.current_dvd = dvd
        self.amplifier.set_dvd(dvd)
        print(f"{self.description} playing {dvd}")

    def stop(self):
        print(f"{self.description} stopped {self.current_dvd}")
        self.current_dvd = None

class Projector:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.input = None

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_input(self, input_type):
        self.input = input_type
        print(f"{self.description} set input to {input_type}")

class HomeTheaterControl:
    def __init__(self, amp, dvd, projector):
        self.amplifier = amp
        self.dvd_player = dvd
        self.projector = projector

    def watch_movie(self, movie):
        if not movie:
            raise ValueError("Movie title cannot be empty")
        print("Get ready to watch a movie...")
        self.projector.on()
        self.projector.set_input("DVD")
        self.amplifier.on()
        self.amplifier.set_volume(5)
        self.dvd_player.on()
        self.dvd_player.play(movie)

    def end_movie(self):
        print("Shutting down the theater...")
        self.dvd_player.stop()
        self.dvd_player.off()
        self.amplifier.off()
        self.projector.off()

if __name__ == "__main__":
    amp = Amplifier("Top-O-Line Amplifier")
    dvd = DvdPlayer("Top-O-Line DVD Player", amp)
    proj = Projector("Top-O-Line Projector", amp)
    control = HomeTheaterControl(amp, dvd, proj)
    control.watch_movie("Inception")
    control.end_movie()