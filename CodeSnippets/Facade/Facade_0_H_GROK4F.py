class Amplifier:
    def __init__(self):
        self.volume = 5
        self.is_on = False

    def power_on(self):
        self.is_on = True
        print("Amplifier is on")

    def set_stereo_volume(self, level):
        if not self.is_on:
            raise ValueError("Amplifier must be on to set volume")
        self.volume = max(0, min(10, level))
        print(f"Amplifier volume set to {self.volume}")

    def power_off(self):
        self.is_on = False
        print("Amplifier is off")

class DvdPlayer:
    def __init__(self, amplifier):
        self.amplifier = amplifier
        self.is_on = False
        self.current_movie = None

    def power_on(self):
        self.is_on = True
        print("DVD player is on")

    def play_movie(self, movie):
        if not self.is_on:
            raise ValueError("DVD player must be on to play")
        self.current_movie = movie
        print(f"Playing movie: {movie}")

    def stop_playback(self):
        if self.current_movie:
            print(f"Stopping movie: {self.current_movie}")
            self.current_movie = None

    def power_off(self):
        self.stop_playback()
        self.is_on = False
        print("DVD player is off")

class Projector:
    def __init__(self):
        self.is_on = False
        self.input_source = None
        self.mode = "normal"

    def power_on(self):
        self.is_on = True
        print("Projector is on")

    def set_input_hdmi(self):
        if not self.is_on:
            raise ValueError("Projector must be on to set input")
        self.input_source = "HDMI"
        print("Projector input set to HDMI")

    def set_wide_mode(self):
        if not self.is_on:
            raise ValueError("Projector must be on to set mode")
        self.mode = "wide"
        print("Projector set to wide screen mode")

    def power_off(self):
        self.is_on = False
        self.input_source = None
        self.mode = "normal"
        print("Projector is off")

class MediaCenterController:
    def __init__(self, amplifier, dvd_player, projector):
        if not all([amplifier, dvd_player, projector]):
            raise ValueError("All components must be provided")
        self.amplifier = amplifier
        self.dvd_player = dvd_player
        self.projector = projector
        self.is_active = False

    def start_movie_session(self, movie_title):
        if self.is_active:
            print("Session already active")
            return
        try:
            self.amplifier.power_on()
            self.projector.power_on()
            self.projector.set_input_hdmi()
            self.projector.set_wide_mode()
            self.dvd_player.power_on()
            self.amplifier.set_stereo_volume(7)
            self.dvd_player.play_movie(movie_title)
            self.is_active = True
            print("Movie session started successfully")
        except ValueError as e:
            self._cleanup_session()
            raise RuntimeError(f"Failed to start session: {str(e)}")

    def end_movie_session(self):
        if not self.is_active:
            print("No active session to end")
            return
        try:
            self.dvd_player.stop_playback()
            self.dvd_player.power_off()
            self.projector.power_off()
            self.amplifier.power_off()
            self.is_active = False
            print("Movie session ended")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def _cleanup_session(self):
        try:
            self.dvd_player.power_off()
            self.projector.power_off()
            self.amplifier.power_off()
            self.is_active = False
        except Exception:
            pass

if __name__ == "__main__":
    amp = Amplifier()
    player = DvdPlayer(amp)
    proj = Projector()
    controller = MediaCenterController(amp, player, proj)
    controller.start_movie_session("Inception")
    controller.end_movie_session()