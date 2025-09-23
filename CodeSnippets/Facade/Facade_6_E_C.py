class AudioSystem:
    def turn_on(self):
        print("Audio system on")
    
    def set_volume(self, level):
        print(f"Volume set to {level}")

class VideoSystem:
    def turn_on(self):
        print("Video system on")
    
    def set_resolution(self, res):
        print(f"Resolution set to {res}")

class LightingSystem:
    def dim_lights(self):
        print("Lights dimmed")

class HomeTheater:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lighting = LightingSystem()
    
    def watch_movie(self):
        self.audio.turn_on()
        self.audio.set_volume(8)
        self.video.turn_on()
        self.video.set_resolution("1080p")
        self.lighting.dim_lights()
        print("Movie ready!")

if __name__ == "__main__":
    theater = HomeTheater()
    theater.watch_movie()