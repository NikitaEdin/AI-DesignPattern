import sys

class Amplifier:
    def __init__(self, description):
        self.description = description
        self.volume = 5

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_stereo_sound(self):
        print(f"{self.description} setting stereo sound")

    def set_volume(self, level):
        self.volume = level
        print(f"{self.description} setting volume to {level}")

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
        self.amplifier.set_stereo_sound()
        print(f"{self.description} playing {movie}")

    def stop(self):
        print(f"{self.description} stopped {self.current_movie}")
        self.current_movie = None

    def eject(self):
        print(f"{self.description} eject")

class Projector:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.input = None
        self.widescreen = False

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_input(self, input_type):
        self.input = input_type
        print(f"{self.description} input set to {input_type}")

    def widescreen_mode(self):
        self.widescreen = True
        print(f"{self.description} widescreen mode")

class TheaterLights:
    def __init__(self, description):
        self.description = description
        self.dim_level = 100

    def dim(self, level):
        self.dim_level = level
        print(f"{self.description} dimming to {level}%")

    def on(self):
        print(f"{self.description} on")

class Screen:
    def __init__(self, description):
        self.description = description
        self.down = False

    def down(self):
        print(f"{self.description} down")
        self.down = True

    def up(self):
        print(f"{self.description} up")
        self.down = False

class HomeTheaterControl:
    def __init__(self, amp, dvd, projector, lights, screen):
        self.amp = amp
        self.dvd = dvd
        self.projector = projector
        self.lights = lights
        self.screen = screen
        self.popcorn = None  # Placeholder for edge case
        self.is_playing = False

    def watch_movie(self, movie):
        try:
            if not movie or not isinstance(movie, str):
                raise ValueError("Invalid movie title provided")
            self._start_movie(movie)
            self.is_playing = True
        except ValueError as e:
            print(f"Error starting movie: {e}")
            self._end_movie()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self._end_movie()

    def end_movie(self):
        if self.is_playing:
            self._end_movie()
            self.is_playing = False

    def _start_movie(self, movie):
        self.popcorn = "popped"  # Simulate preparation
        if self.popcorn != "popped":
            raise RuntimeError("Popcorn not ready")
        self.lights.on()
        self.lights.dim(10)
        self.screen.down()
        self.projector.on()
        self.projector.set_input("DVD")
        self.projector.widescreen_mode()
        self.amp.on()
        self.amp.set_stereo_sound()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)

    def _end_movie(self):
        if self.is_playing:
            self.dvd.stop()
            self.dvd.off()
            self.amp.off()
            self.projector.off()
            self.lights.on()
            self.screen.up()
            if self.popcorn:
                self.popcorn = None

if __name__ == "__main__":
    amp = Amplifier("Top-O-Line Amplifier")
    dvd = DvdPlayer("Top-O-Line DVD Player", amp)
    projector = Projector("Top-O-Line Projector", amp)
    lights = TheaterLights("Theater Lights")
    screen = Screen("Theater Screen")

    control = HomeTheaterControl(amp, dvd, projector, lights, screen)

    control.watch_movie("The Matrix")
    print("---")
    control.end_movie()

    # Edge case: invalid movie
    print("---")
    control.watch_movie("")