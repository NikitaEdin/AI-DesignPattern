class AudioSystem:
    def __init__(self):
        self.volume = 0
    
    def turn_on(self):
        print("Audio system powered on")
    
    def set_volume(self, level):
        self.volume = level
        print(f"Audio volume set to {level}")
    
    def turn_off(self):
        print("Audio system powered off")

class VideoProjector:
    def __init__(self):
        self.brightness = 0
    
    def power_on(self):
        print("Video projector started")
    
    def set_brightness(self, level):
        self.brightness = level
        print(f"Projector brightness set to {level}")
    
    def power_off(self):
        print("Video projector shut down")

class LightingSystem:
    def __init__(self):
        self.dimmed = False
    
    def dim_lights(self):
        self.dimmed = True
        print("Lights dimmed for viewing")
    
    def normal_lights(self):
        self.dimmed = False
        print("Lights restored to normal")

class HomeTheater:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
    
    def start_movie(self, volume=7, brightness=8):
        try:
            print("Starting movie experience...")
            self.lights.dim_lights()
            self.audio.turn_on()
            self.audio.set_volume(volume)
            self.projector.power_on()
            self.projector.set_brightness(brightness)
            print("Movie ready to play!")
        except Exception as e:
            print(f"Error starting movie: {e}")
    
    def end_movie(self):
        print("Ending movie experience...")
        self.projector.power_off()
        self.audio.turn_off()
        self.lights.normal_lights()
        print("All systems shut down")

if __name__ == "__main__":
    theater = HomeTheater()
    theater.start_movie(volume=8, brightness=9)
    print()
    theater.end_movie()