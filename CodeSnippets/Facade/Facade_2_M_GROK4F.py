class Amplifier:
    def on(self):
        print("Amplifier is on")
    
    def set_stereo_volume(self, level):
        print(f"Setting stereo volume to {level}")
    
    def off(self):
        print("Amplifier is off")

class DvdPlayer:
    def on(self):
        print("DVD player is on")
    
    def play(self, movie):
        if not isinstance(movie, str):
            raise ValueError("Movie must be a string")
        print(f"Playing movie: {movie}")
    
    def off(self):
        print("DVD player is off")

class Projector:
    def on(self):
        print("Projector is on")
    
    def set_input(self, source):
        print(f"Projector input set to {source}")
    
    def wide_screen_mode(self):
        print("Projector switched to widescreen mode")
    
    def off(self):
        print("Projector is off")

class HomeTheater:
    def __init__(self, amplifier, dvd_player, projector):
        self.amplifier = amplifier
        self.dvd_player = dvd_player
        self.projector = projector
    
    def watch_movie(self, movie):
        print("Preparing to watch a movie...")
        self.projector.on()
        self.projector.set_input("DVD")
        self.projector.wide_screen_mode()
        self.amplifier.on()
        self.amplifier.set_stereo_volume(5)
        self.dvd_player.on()
        self.dvd_player.play(movie)
    
    def end_movie(self):
        print("Ending the movie session...")
        self.dvd_player.off()
        self.amplifier.off()
        self.projector.off()

if __name__ == "__main__":
    amp = Amplifier()
    dvd = DvdPlayer()
    proj = Projector()
    
    theater = HomeTheater(amp, dvd, proj)
    theater.watch_movie("The Matrix")
    theater.end_movie()