class VideoPlayer:
    def __init__(self):
        self.is_on = False

    def power_on(self):
        self.is_on = True
        print("Video player powered on.")

    def power_off(self):
        self.is_on = False
        print("Video player powered off.")

    def play(self, movie):
        if self.is_on:
            print(f"Playing movie: {movie}")
        else:
            raise ValueError("Video player must be on to play.")

    def stop(self):
        if self.is_on:
            print("Stopped playing.")
        else:
            raise ValueError("Video player must be on to stop.")

class AudioSystem:
    def __init__(self):
        self.is_on = False
        self.volume = 0

    def power_on(self):
        self.is_on = True
        print("Audio system powered on.")

    def power_off(self):
        self.is_on = False
        print("Audio system powered off.")

    def set_volume(self, level):
        if self.is_on:
            self.volume = level
            print(f"Volume set to {level}.")
        else:
            raise ValueError("Audio system must be on to adjust volume.")

class Display:
    def __init__(self):
        self.is_on = False

    def power_on(self):
        self.is_on = True
        print("Display powered on.")

    def power_off(self):
        self.is_on = False
        print("Display powered off.")

    def set_input(self, source):
        if self.is_on:
            print(f"Display input set to {source}.")
        else:
            raise ValueError("Display must be on to set input.")

class MediaCenter:
    def __init__(self, video_player, audio_system, display):
        self.video_player = video_player
        self.audio_system = audio_system
        self.display = display

    def watch_movie(self, movie):
        try:
            self.display.power_on()
            self.display.set_input("video_player")
            self.video_player.power_on()
            self.audio_system.power_on()
            self.audio_system.set_volume(5)
            self.video_player.play(movie)
        except ValueError as e:
            print(f"Error during movie setup: {e}")
            self.shutdown()

    def end_movie(self):
        try:
            self.video_player.stop()
            self.video_player.power_off()
            self.audio_system.power_off()
            self.display.power_off()
            print("Movie session ended.")
        except ValueError as e:
            print(f"Error during shutdown: {e}")

    def shutdown(self):
        self.video_player.power_off()
        self.audio_system.power_off()
        self.display.power_off()

if __name__ == "__main__":
    video = VideoPlayer()
    audio = AudioSystem()
    disp = Display()
    center = MediaCenter(video, audio, disp)
    center.watch_movie("Inception")
    center.end_movie()