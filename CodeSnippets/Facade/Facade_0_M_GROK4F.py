class Amplifier:
    def __init__(self):
        self.volume = 0

    def power_on(self):
        print("Amplifier powered on")

    def set_input(self, source):
        print(f"Amplifier input set to {source}")

    def set_volume(self, level):
        self.volume = level
        print(f"Amplifier volume set to {level}")

    def power_off(self):
        print("Amplifier powered off")

class DvdPlayer:
    def __init__(self):
        self.is_playing = False

    def power_on(self):
        print("DVD player powered on")

    def play(self, title):
        if title:
            self.is_playing = True
            print(f"DVD player playing '{title}'")
        else:
            raise ValueError("No movie title provided")

    def stop(self):
        self.is_playing = False
        print("DVD player stopped")

    def power_off(self):
        print("DVD player powered off")

class Projector:
    def power_on(self):
        print("Projector powered on")

    def set_input(self, source):
        print(f"Projector input set to {source}")

    def set_mode(self, mode):
        print(f"Projector mode set to {mode}")

    def power_off(self):
        print("Projector powered off")

class HomeTheaterController:
    def __init__(self, amplifier, dvd_player, projector):
        self.amplifier = amplifier
        self.dvd_player = dvd_player
        self.projector = projector

    def start_movie(self, movie_title):
        try:
            self.projector.power_on()
            self.projector.set_input("DVD")
            self.projector.set_mode("widescreen")
            self.amplifier.power_on()
            self.amplifier.set_input("projector")
            self.amplifier.set_volume(5)
            self.dvd_player.power_on()
            self.dvd_player.play(movie_title)
        except ValueError as e:
            print(f"Error starting movie: {e}")
            self.stop_movie()

    def stop_movie(self):
        self.dvd_player.stop()
        self.dvd_player.power_off()
        self.amplifier.power_off()
        self.projector.power_off()

if __name__ == "__main__":
    amp = Amplifier()
    dvd = DvdPlayer()
    proj = Projector()
    controller = HomeTheaterController(amp, dvd, proj)
    controller.start_movie("Inception")
    controller.stop_movie()