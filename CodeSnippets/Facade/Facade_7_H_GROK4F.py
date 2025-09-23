class Amplifier:
    def __init__(self, description):
        self.description = description
        self.volume = 5

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_stereo_volume(self, volume):
        self.volume = volume
        print(f"{self.description} stereo volume set to {volume}")

    def set_surround_volume(self, volume):
        self.volume = volume
        print(f"{self.description} surround volume set to {volume}")

class DvdPlayer:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.current_movie = None

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def play(self, movie):
        self.current_movie = movie
        self.amplifier.set_surround_volume(5)
        print(f"{self.description} playing {movie.title}")

    def stop(self):
        print(f"{self.description} stopped {self.current_movie.title}")
        self.current_movie = None

    def eject(self):
        print(f"{self.description} ejecting {self.current_movie.title}")
        self.stop()

class Projector:
    def __init__(self, description, quality_setting="1080p"):
        self.description = description
        self.quality_setting = quality_setting
        self.input = None

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_input(self, input_type):
        self.input = input_type
        print(f"{self.description} input set to {input_type}")

    def wide_screen_mode(self):
        print(f"{self.description} in widescreen mode ({self.quality_setting})")

class Movie:
    def __init__(self, title):
        self.title = title

class HomeTheaterControl:
    def __init__(self, amp, dvd, projector):
        self.amp = amp
        self.dvd = dvd
        self.projector = projector
        self.is_on = False
        self.popcorn_ready = False

    def start_movie(self, movie):
        if not self.is_on:
            print("Error: System is off. Cannot start movie.")
            return False
        if not self.popcorn_ready:
            print("Warning: Popcorn not ready. Proceeding anyway.")
        try:
            self.popcorn_ready = True
            print("Popping popcorn...")
            self.amp.on()
            self.amp.set_surround_volume(5)
            self.projector.on()
            self.projector.set_input("DVD")
            self.projector.wide_screen_mode()
            self.dvd.on()
            self.dvd.play(movie)
            self.is_on = True
            return True
        except AttributeError as e:
            print(f"Error initializing devices: {e}")
            self.end_movie()
            return False

    def end_movie(self):
        if not self.is_on:
            return
        try:
            self.dvd.stop()
            self.dvd.off()
            self.projector.off()
            self.amp.off()
            self.is_on = False
            print("Movie ended.")
        except AttributeError as e:
            print(f"Error shutting down: {e}")

    def power_on(self):
        if self.is_on:
            return
        self.amp.on()
        self.dvd.on()
        self.projector.on()
        self.is_on = True
        print("System powered on.")

    def power_off(self):
        if not self.is_on:
            return
        self.end_movie()
        self.is_on = False
        print("System powered off.")

    def set_volume(self, volume):
        if 0 <= volume <= 10:
            self.amp.set_stereo_volume(volume)
        else:
            print("Error: Volume must be between 0 and 10.")

if __name__ == "__main__":
    amp = Amplifier("Top-O-Line Amplifier")
    projector = Projector("Top-O-Line Projector")
    dvd = DvdPlayer("Top-O-Line DVD Player", amp)

    control = HomeTheaterControl(amp, dvd, projector)

    control.power_on()
    movie = Movie("Inception")
    control.start_movie(movie)
    control.set_volume(7)
    control.end_movie()
    control.power_off()