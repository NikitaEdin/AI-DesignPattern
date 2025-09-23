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

class LightSystem:
    def dim_lights(self):
        print("Lights dimmed")

class HomeTheater:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lights = LightSystem()
    
    def watch_movie(self):
        self.lights.dim_lights()
        self.audio.turn_on()
        self.audio.set_volume(8)
        self.video.turn_on()
        self.video.set_resolution("4K")

if __name__ == "__main__":
    theater = HomeTheater()
    theater.watch_movie()