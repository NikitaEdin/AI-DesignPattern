class Amplifier:
    def __init__(self, description):
        self.description = description
        self.volume = 5

    def on(self):
        print(f"{self.description} is on")

    def off(self):
        print(f"{self.description} is off")

    def set_stereo_sound(self):
        print(f"{self.description} setting stereo sound")

    def set_volume(self, volume):
        self.volume = volume
        if 0 <= volume <= 11:
            print(f"{self.description} setting volume to {volume}")
        else:
            print(f"{self.description} volume out of range, defaulting to 5")
            self.volume = 5

class DvdPlayer:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.current_movie = None

    def on(self):
        print(f"{self.description} is on")

    def off(self):
        print(f"{self.description} is off")

    def play(self, movie):
        self.current_movie = movie
        self.amplifier.set_volume(7)
        print(f"{self.description} playing {movie.title}")

    def pause(self):
        if self.current_movie:
            print(f"{self.description} paused {self.current_movie.title}")
        else:
            print(f"{self.description} no movie to pause")

    def stop(self):
        if self.current_movie:
            print(f"{self.description} stopped {self.current_movie.title}")
            self.current_movie = None
        else:
            print(f"{self.description} already stopped")

class Projector:
    def __init__(self, description, amplifier=None):
        self.description = description
        self.amplifier = amplifier
        self.input = None
        self.tv_mode = False

    def on(self):
        print(f"{self.description} is on")

    def off(self):
        print(f"{self.description} is off")

    def set_input(self, input_type):
        if input_type in ['dvd', 'hdmi', 'blu-ray']:
            self.input = input_type
            print(f"{self.description} input set to {input_type}")
        else:
            print(f"{self.description} invalid input {input_type}, defaulting to hdmi")
            self.input = 'hdmi'

    def wide_screen_mode(self):
        if not self.tv_mode:
            print(f"{self.description} in widescreen mode")
        else:
            print(f"{self.description} already in TV mode, ignoring widescreen")

class TheaterLights:
    def __init__(self, description):
        self.description = description
        self.dim_level = 100

    def on(self):
        print(f"{self.description} lights are on")

    def off(self):
        print(f"{self.description} lights are off")

    def dim(self, level):
        if 0 <= level <= 100:
            self.dim_level = level
            print(f"{self.description} lights dimmed to {level}%")
        else:
            print(f"{self.description} dim level out of range, defaulting to 50%")
            self.dim_level = 50

class Screen:
    def __init__(self, description):
        self.description = description
        self.rolled_up = True

    def up(self):
        if self.rolled_up:
            print(f"{self.description} going up")
            self.rolled_up = False
        else:
            print(f"{self.description} already up")

    def down(self):
        if not self.rolled_up:
            print(f"{self.description} going down")
            self.rolled_up = True
        else:
            print(f"{self.description} already down")

class CinemaSystemManager:
    def __init__(self, amp, dvd, projector, lights, screen):
        self.amplifier = amp
        self.dvd_player = dvd
        self.projector = projector
        self.lights = lights
        self.screen = screen

    def watch_movie(self, movie):
        try:
            print("Get ready to watch a movie...")
            self.lights.off()
            self.screen.down()
            self.projector.on()
            self.projector.set_input('dvd')
            self.projector.wide_screen_mode()
            self.amplifier.on()
            self.amplifier.set_stereo_sound()
            self.dvd_player.on()
            self.dvd_player.play(movie)
        except Exception as e:
            print(f"Error during movie setup: {e}")
            self.end_movie()

    def end_movie(self):
        try:
            print("Shutting down the cinema system...")
            if self.dvd_player.current_movie:
                self.dvd_player.stop()
            self.dvd_player.off()
            self.lights.on()
            self.lights.dim(50)
            self.projector.off()
            self.amplifier.off()
            self.screen.up()
        except Exception as e:
            print(f"Error during shutdown: {e}")

class Movie:
    def __init__(self, title):
        self.title = title

if __name__ == "__main__":
    amp = Amplifier("Top-O-Line Amplifier")
    dvd = DvdPlayer("Top-O-Line DVD Player", amp)
    projector = Projector("Top-O-Line Projector", amp)
    lights = TheaterLights("Theater Lights")
    screen = Screen("Projector Screen")

    manager = CinemaSystemManager(amp, dvd, projector, lights, screen)
    movie = Movie("Inception")

    manager.watch_movie(movie)
    print("\n" + "="*50 + "\n")
    manager.end_movie()