class AudioSystem:
    def __init__(self):
        self.volume = 50
    
    def turn_on(self):
        return "Audio system powered on"
    
    def set_volume(self, level):
        self.volume = max(0, min(100, level))
        return f"Volume set to {self.volume}"
    
    def turn_off(self):
        return "Audio system powered off"

class VideoProjector:
    def __init__(self):
        self.brightness = 75
    
    def power_on(self):
        return "Projector powered on"
    
    def set_input(self, source):
        return f"Input set to {source}"
    
    def power_off(self):
        return "Projector powered off"

class LightingSystem:
    def __init__(self):
        self.brightness = 100
    
    def dim_lights(self, level):
        self.brightness = max(0, min(100, level))
        return f"Lights dimmed to {self.brightness}%"
    
    def restore_lights(self):
        self.brightness = 100
        return "Lights restored to full brightness"

class HomeTheaterController:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
    
    def start_movie(self, volume=70):
        results = []
        results.append(self.lights.dim_lights(20))
        results.append(self.projector.power_on())
        results.append(self.projector.set_input("Blu-ray"))
        results.append(self.audio.turn_on())
        results.append(self.audio.set_volume(volume))
        return results
    
    def end_movie(self):
        results = []
        results.append(self.audio.turn_off())
        results.append(self.projector.power_off())
        results.append(self.lights.restore_lights())
        return results

if __name__ == "__main__":
    theater = HomeTheaterController()
    
    print("Starting movie night:")
    for action in theater.start_movie(80):
        print(f"- {action}")
    
    print("\nEnding movie night:")
    for action in theater.end_movie():
        print(f"- {action}")