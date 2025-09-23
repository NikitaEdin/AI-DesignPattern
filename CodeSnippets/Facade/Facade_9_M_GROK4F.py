class Light:
    def dim(self, level):
        print(f"Light dimmed to {level}%")
    
    def brighten(self):
        print("Light brightened")

class Projector:
    def on(self):
        print("Projector turned on")
    
    def off(self):
        print("Projector turned off")
    
    def set_input(self, input_source):
        print(f"Projector set to {input_source}")

class Amplifier:
    def on(self):
        print("Amplifier turned on")
    
    def set_stereo_volume(self, level):
        print(f"Amplifier stereo volume set to {level}")
    
    def off(self):
        print("Amplifier turned off")

class DvdPlayer:
    def on(self):
        print("DVD player turned on")
    
    def play(self, movie):
        print(f"DVD player playing {movie}")
    
    def off(self):
        print("DVD player turned off")

class HomeTheater:
    def __init__(self):
        self.light = Light()
        self.projector = Projector()
        self.amplifier = Amplifier()
        self.player = DvdPlayer()
    
    def watch_movie(self, movie):
        try:
            self.light.dim(10)
            self.projector.on()
            self.projector.set_input("DVD")
            self.amplifier.on()
            self.amplifier.set_stereo_volume(5)
            self.player.on()
            self.player.play(movie)
            print("Enjoy the show!")
        except Exception as e:
            print(f"Error setting up theater: {e}")
            self.end_movie()
    
    def end_movie(self):
        try:
            self.player.off()
            self.amplifier.off()
            self.projector.off()
            self.light.brighten()
            print("Movie ended.")
        except Exception as e:
            print(f"Error ending movie: {e}")

if __name__ == "__main__":
    theater = HomeTheater()
    theater.watch_movie("Inception")
    theater.end_movie()