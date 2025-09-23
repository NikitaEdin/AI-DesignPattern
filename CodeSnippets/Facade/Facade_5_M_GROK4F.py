class Amplifier:
    def on(self):
        print("Amplifier is on")

    def set_stereo_volume(self, level):
        print(f"Amplifier volume set to {level}")

    def off(self):
        print("Amplifier is off")

class DvdPlayer:
    def on(self):
        print("DVD player is on")

    def play(self, movie):
        print(f"Playing {movie} on DVD player")

    def off(self):
        print("DVD player is off")

class Projector:
    def on(self):
        print("Projector is on")

    def set_input(self, source):
        print(f"Projector input set to {source}")

    def off(self):
        print("Projector is off")

class HomeTheater:
    def __init__(self, amp, dvd, proj):
        self.amp = amp
        self.dvd = dvd
        self.proj = proj

    def watch_movie(self, movie):
        try:
            if not all([self.amp, self.dvd, self.proj]):
                raise ValueError("Missing home theater components")
            self.proj.on()
            self.proj.set_input("DVD")
            self.amp.on()
            self.amp.set_stereo_volume(5)
            self.dvd.on()
            self.dvd.play(movie)
            print("Enjoy the show!")
        except ValueError as e:
            print(f"Error: {e}")
        finally:
            pass  # Cleanup could be added here

if __name__ == "__main__":
    amp = Amplifier()
    dvd = DvdPlayer()
    proj = Projector()
    theater = HomeTheater(amp, dvd, proj)
    theater.watch_movie("Inception")