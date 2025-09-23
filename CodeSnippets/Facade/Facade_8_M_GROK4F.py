class Projector:
    def __init__(self):
        self.current_mode = None

    def on(self):
        print("Projector on")

    def set_input(self, input_source):
        self.current_mode = input_source
        print(f"Projector set to {input_source}")

    def off(self):
        print("Projector off")

class Amplifier:
    def __init__(self):
        self.volume = 0

    def on(self):
        print("Amplifier on")

    def set_stereo_volume(self, volume):
        self.volume = volume
        print(f"Amplifier volume set to {volume}")

    def off(self):
        print("Amplifier off")

class DvdPlayer:
    def __init__(self, amp, projector):
        self.amp = amp
        self.projector = projector
        self.current_dvd = None

    def on(self):
        self.amp.on()
        self.projector.on()
        print("DVD Player on")

    def play(self, movie):
        if not isinstance(movie, str):
            raise ValueError("Movie title must be a string")
        self.current_dvd = movie
        self.projector.set_input("DVD")
        self.amp.set_stereo_volume(5)
        print(f"Playing {movie}")

    def off(self):
        print("DVD Player off")
        self.amp.off()
        self.projector.off()

class MediaCenter:
    def __init__(self, amp, projector):
        self.amp = amp
        self.projector = projector
        self.dvd_player = DvdPlayer(amp, projector)

    def watch_movie(self, movie_title):
        try:
            self.dvd_player.on()
            self.dvd_player.play(movie_title)
        except ValueError as e:
            print(f"Error: {e}")

    def end_movie(self):
        self.dvd_player.off()

if __name__ == "__main__":
    amp = Amplifier()
    projector = Projector()
    center = MediaCenter(amp, projector)
    center.watch_movie("Inception")
    center.end_movie()