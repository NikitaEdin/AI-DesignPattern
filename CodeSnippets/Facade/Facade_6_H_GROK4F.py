class Amplifier:
    def __init__(self, description):
        self.description = description
        self.volume = 5

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_stereo_volume(self, volume):
        if not 0 <= volume <= 10:
            raise ValueError("Volume must be between 0 and 10")
        self.volume = volume
        print(f"{self.description} stereo volume set to {volume}")

    def set_surround_volume(self, volume):
        if not 0 <= volume <= 10:
            raise ValueError("Volume must be between 0 and 10")
        self.volume = volume
        print(f"{self.description} surround volume set to {volume}")

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
        if movie is None:
            raise ValueError("No movie selected")
        self.current_movie = movie
        self.amplifier.set_surround_volume(5)
        print(f"{self.description} playing {movie.title if hasattr(movie, 'title') else movie}")

    def stop(self):
        if self.current_movie:
            print(f"{self.description} stopped {self.current_movie}")
            self.current_movie = None

    def set_surround_audio(self):
        print(f"{self.description} surround audio engaged")

class Projector:
    def __init__(self, description, screen):
        self.description = description
        self.screen = screen

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_input(self, device):
        print(f"{self.description} input set to {device.description}")

    def wide_screen_mode(self):
        print(f"{self.description} in widescreen mode")

class Screen:
    def __init__(self, description):
        self.description = description
        self.positioned_down = False

    def down(self):
        if not self.positioned_down:
            print(f"{self.description} descending")
            self.positioned_down = True
        else:
            print(f"{self.description} already down")

    def up(self):
        if self.positioned_down:
            print(f"{self.description} ascending")
            self.positioned_down = False
        else:
            print(f"{self.description} already up")

class TheaterLights:
    def __init__(self, description):
        self.description = description
        self.intensity = 100

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def dim(self, level):
        if not 0 <= level <= 100:
            raise ValueError("Light level must be between 0 and 100")
        self.intensity = level
        print(f"{self.description} dimmed to {level}%")

class HomeTheater:
    def __init__(self, amplifier, dvd_player, projector, lights, screen):
        self.amplifier = amplifier
        self.dvd_player = dvd_player
        self.projector = projector
        self.lights = lights
        self.screen = screen

    def watch_movie(self, movie):
        try:
            print("\n--- Starting movie ---")
            self.lights.dim(10)
            self.screen.down()
            self.projector.on()
            self.projector.set_input(self.dvd_player)
            self.projector.wide_screen_mode()
            self.amplifier.on()
            self.amplifier.set_surround_volume(5)
            self.dvd_player.on()
            self.dvd_player.set_surround_audio()
            self.dvd_player.play(movie)
        except ValueError as e:
            print(f"Operation failed: {e}")
            self.shutdown()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.shutdown()

    def end_movie(self):
        print("\n--- Ending movie ---")
        self.dvd_player.stop()
        self.dvd_player.off()
        self.lights.on()
        self.screen.up()
        self.projector.off()
        self.amplifier.off()

    def shutdown(self):
        self.end_movie()

class Movie:
    def __init__(self, title):
        self.title = title

if __name__ == "__main__":
    amplifier = Amplifier("Premium Amplifier")
    dvd_player = DvdPlayer("High-End DVD Player", amplifier)
    screen = Screen("Large Projection Screen")
    projector = Projector("Advanced Projector", screen)
    lights = TheaterLights("Ambient Theater Lights")

    theater = HomeTheater(amplifier, dvd_player, projector, lights, screen)

    movie = Movie("Inception")
    theater.watch_movie(movie)
    theater.end_movie()

    print("\n--- Demonstrating edge case ---")
    theater.watch_movie(None)