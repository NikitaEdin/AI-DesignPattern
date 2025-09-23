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

class DvdPlayer:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.current_movie = None
        self.is_on = False

    def on(self):
        print(f"{self.description} on")
        self.is_on = True
        self.amplifier.on()

    def off(self):
        print(f"{self.description} off")
        self.is_on = False
        self.amplifier.off()

    def play(self, movie):
        if not self.is_on:
            raise ValueError("DVD player must be on to play")
        if not movie:
            raise ValueError("Movie cannot be empty")
        self.current_movie = movie
        print(f"{self.description} playing {movie}")

    def stop(self):
        if self.current_movie:
            print(f"{self.description} stopped {self.current_movie}")
            self.current_movie = None

class Projector:
    def __init__(self, description, input_source):
        self.description = description
        self.input_source = input_source
        self.is_on = False

    def on(self):
        print(f"{self.description} on")
        self.is_on = True

    def off(self):
        print(f"{self.description} off")
        self.is_on = False

    def set_input(self, input_source):
        self.input_source = input_source
        print(f"{self.description} input set to {input_source}")

    def wide_screen_mode(self):
        if not self.is_on:
            raise ValueError("Projector must be on for wide screen mode")
        print(f"{self.description} in widescreen mode")

class HomeTheaterControl:
    def __init__(self, amplifier, dvd_player, projector):
        if not all([amplifier, dvd_player, projector]):
            raise ValueError("All components must be provided")
        self.amplifier = amplifier
        self.dvd_player = dvd_player
        self.projector = projector
        self.is_watching_movie = False

    def watch_movie(self, movie):
        if self.is_watching_movie:
            raise RuntimeError("Already watching a movie")
        if not movie or not isinstance(movie, str):
            raise ValueError("Valid movie title required")
        try:
            self.projector.on()
            self.projector.set_input(self.dvd_player.description)
            self.projector.wide_screen_mode()
            self.amplifier.on()
            self.amplifier.set_stereo_volume(5)
            self.dvd_player.on()
            self.dvd_player.play(movie)
            self.is_watching_movie = True
            print("Enjoy the show!")
        except Exception as e:
            self._shutdown()
            raise RuntimeError(f"Failed to start movie: {e}")

    def end_movie(self):
        if not self.is_watching_movie:
            print("No movie currently playing")
            return
        self._shutdown()
        self.is_watching_movie = False
        print("Shutting down theater")

    def _shutdown(self):
        try:
            self.dvd_player.stop()
            self.dvd_player.off()
            self.projector.off()
            self.amplifier.off()
        except Exception:
            pass  # Ignore shutdown errors to prevent cascading failures

if __name__ == "__main__":
    amp = Amplifier("Top-O-Line Amplifier")
    player = DvdPlayer("Top-O-Line DVD Player", amp)
    proj = Projector("Top-O-Line Projector", "DVD")
    theater = HomeTheaterControl(amp, player, proj)
    theater.watch_movie("Avengers")
    theater.end_movie()