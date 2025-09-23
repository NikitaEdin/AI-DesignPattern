import sys

class Amplifier:
    def __init__(self, description):
        self.description = description
        self.volume = 5

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_dvd(self, dvd):
        print(f"{self.description} setting DVD player to {dvd}")

    def set_stereo_sound(self):
        print(f"{self.description} stereo mode on")

    def set_volume(self, volume):
        if 0 <= volume <= 11:
            self.volume = volume
            print(f"{self.description} being volume set to {volume}")
        else:
            raise ValueError("Volume must be between 0 and 11")

class Tuner:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_frequency(self, frequency):
        print(f"{self.description} setting frequency to {frequency}")
        self.amplifier.set_volume(5)

class DvdPlayer:
    def __init__(self, description, amplifier):
        self.description = description
        self.amplifier = amplifier
        self.current_dvd = None

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def play(self, movie):
        self.current_dvd = movie
        self.amplifier.set_dvd(self.description)
        print(f"{self.description} playing {movie}")

    def stop(self):
        if self.current_dvd:
            print(f"{self.description} stopped {self.current_dvd}")
            self.current_dvd = None
        else:
            print(f"{self.description} no DVD to stop")

    def pause(self):
        if self.current_dvd:
            print(f"{self.description} paused {self.current_dvd}")
        else:
            print(f"{self.description} cannot pause: no DVD playing")

class Projector:
    def __init__(self, description, dvd_player):
        self.description = description
        self.dvd_player = dvd_player
        self.resolution = "1080p"

    def on(self):
        print(f"{self.description} on")

    def off(self):
        print(f"{self.description} off")

    def set_input(self, input_device):
        print(f"{self.description} input set to {input_device}")

    def set_resolution(self, res):
        valid_res = ["720p", "1080p", "4K"]
        if res in valid_res:
            self.resolution = res
            print(f"{self.description} resolution set to {res}")
        else:
            raise ValueError(f"Invalid resolution: {res}. Must be one of {valid_res}")

class TheaterLights:
    def __init__(self, description):
        self.description = description
        self.brightness = 100

    def dim(self, level):
        if 0 <= level <= 100:
            self.brightness = level
            print(f"{self.description} dimming to {level}%")
        else:
            raise ValueError("Brightness level must be between 0 and 100")

    def on(self):
        print(f"{self.description} on")

class Screen:
    def __init__(self, description):
        self.description = description
        self.position = "up"

    def down(self):
        if self.position == "up":
            self.position = "down"
            print(f"{self.description} down")
        else:
            print(f"{self.description} already down")

    def up(self):
        if self.position == "down":
            self.position = "up"
            print(f"{self.description} up")
        else:
            print(f"{self.description} already up")

class HomeTheaterManager:
    def __init__(self, amp, tuner, dvd, projector, lights, screen):
        self.amplifier = amp
        self.tuner = tuner
        self.dvd_player = dvd
        self.projector = projector
        self.lights = lights
        self.screen = screen
        self.is_playing = False

    def start_movie(self, movie):
        try:
            if self.is_playing:
                print("Movie already playing")
                return
            self.lights.dim(10)
            self.screen.down()
            self.projector.on()
            self.projector.set_input(self.dvd_player)
            self.projector.set_resolution("1080p")
            self.amplifier.on()
            self.amplifier.set_dvd(self.dvd_player)
            self.amplifier.set_stereo_sound()
            self.dvd_player.on()
            self.dvd_player.play(movie)
            self.is_playing = True
            print(f"Enjoy the show: {movie}")
        except (ValueError, AttributeError) as e:
            print(f"Error starting movie: {e}")
            self.stop_movie()

    def end_movie(self):
        if not self.is_playing:
            print("No movie to end")
            return
        try:
            self.dvd_player.stop()
            self.lights.on()
            self.screen.up()
            self.projector.off()
            self.amplifier.off()
            self.dvd_player.off()
            self.is_playing = False
            print("Movie ended")
        except (ValueError, AttributeError) as e:
            print(f"Error ending movie: {e}")

if __name__ == "__main__":
    amp = Amplifier("Top-O-Line Amplifier")
    tuner = Tuner("Top-O-Line Tuner", amp)
    dvd = DvdPlayer("Top-O-Line DVD Player", amp)
    projector = Projector("Top-O-Line Projector", dvd)
    lights = TheaterLights("Hotspot Lights")
    screen = Screen("Top-O-Line Screen")

    manager = HomeTheaterManager(amp, tuner, dvd, projector, lights, screen)
    manager.start_movie("Inception")
    print("\n" + "="*40 + "\n")
    manager.end_movie()