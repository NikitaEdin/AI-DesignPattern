class AudioAmplifier:
    def __init__(self):
        self.powered = False

    def power_on(self):
        self.powered = True
        print("Audio amplifier powered on")

    def set_stereo_volume(self, volume):
        print(f"Setting stereo volume to {volume}")

    def power_off(self):
        self.powered = False
        print("Audio amplifier powered off")

class VideoProjector:
    def __init__(self):
        self.powered = False
        self.input_source = None

    def power_on(self):
        self.powered = True
        print("Video projector powered on")

    def set_input_hdmi(self):
        self.input_source = "HDMI"
        print("Projector input set to HDMI")

    def power_off(self):
        self.powered = False
        print("Video projector powered off")

class DvdPlayer:
    def __init__(self, amplifier=None, projector=None):
        self.amplifier = amplifier
        self.projector = projector
        self.is_on = False
        self.current_disc = None

    def power_on(self):
        self.is_on = True
        print("DVD player powered on")
        if self.amplifier:
            self.amplifier.power_on()

    def play_disc(self, disc_title):
        if not disc_title:
            raise ValueError("No disc title provided")
        self.current_disc = disc_title
        print(f"Playing DVD: {disc_title}")
        if self.projector:
            self.projector.set_input_hdmi()

    def power_off(self):
        self.is_on = False
        print("DVD player powered off")
        if self.amplifier:
            self.amplifier.power_off()
        if self.projector:
            self.projector.power_off()

class LightingSystem:
    def __init__(self):
        pass

    def dim_to(self, percentage):
        print(f"Dimming lights to {percentage}%")

    def full_brightness(self):
        print("Lights at full brightness")

class MediaCenter:
    def __init__(self, amplifier=None, player=None, projector=None, lights=None):
        self.amplifier = amplifier
        self.player = player
        self.projector = projector
        self.lights = lights

    def start_movie(self, movie_title):
        if not movie_title:
            raise ValueError("Movie title cannot be empty")
        print("--- Starting movie session ---")
        if self.lights:
            self.lights.dim_to(10)
        if self.projector:
            self.projector.power_on()
        if self.player:
            self.player.power_on()
            try:
                self.player.play_disc(movie_title)
            except ValueError as e:
                print(f"Failed to play: {e}")
                self.end_movie()
                return
        if self.amplifier:
            self.amplifier.set_stereo_volume(5)
        print("Enjoy the movie!\n")

    def end_movie(self):
        print("--- Ending movie session ---")
        if self.player:
            self.player.power_off()
        if self.lights:
            self.lights.full_brightness()
        print("Session ended.\n")

if __name__ == "__main__":
    amp = AudioAmplifier()
    proj = VideoProjector()
    lights = LightingSystem()
    player_full = DvdPlayer(amp, proj)
    center_full = MediaCenter(amp, player_full, proj, lights)
    center_full.start_movie("The Matrix")
    center_full.end_movie()

    player_partial = DvdPlayer(projector=proj)
    center_partial = MediaCenter(player=player_partial, projector=proj)
    center_partial.start_movie("Silent Film")
    center_partial.end_movie()

    try:
        center_full.start_movie("")
    except ValueError as e:
        print(f"Error starting session: {e}")