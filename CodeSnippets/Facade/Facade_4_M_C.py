class AudioSystem:
    def __init__(self):
        self.volume = 50
    
    def power_on(self):
        return "Audio system powered on"
    
    def set_volume(self, level):
        self.volume = level
        return f"Volume set to {level}"
    
    def power_off(self):
        return "Audio system powered off"

class VideoProjector:
    def __init__(self):
        self.brightness = 75
    
    def turn_on(self):
        return "Projector turned on"
    
    def set_input(self, source):
        return f"Input set to {source}"
    
    def turn_off(self):
        return "Projector turned off"

class LightingSystem:
    def __init__(self):
        self.brightness = 100
    
    def dim_lights(self, level):
        self.brightness = level
        return f"Lights dimmed to {level}%"
    
    def normal_lights(self):
        self.brightness = 100
        return "Lights restored to normal"

class HomeTheaterController:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
    
    def start_movie(self, source="HDMI"):
        results = []
        results.append(self.lights.dim_lights(20))
        results.append(self.projector.turn_on())
        results.append(self.projector.set_input(source))
        results.append(self.audio.power_on())
        results.append(self.audio.set_volume(75))
        return results
    
    def end_movie(self):
        results = []
        results.append(self.audio.power_off())
        results.append(self.projector.turn_off())
        results.append(self.lights.normal_lights())
        return results

if __name__ == "__main__":
    theater = HomeTheaterController()
    
    print("Starting movie night:")
    for action in theater.start_movie("Blu-ray"):
        print(f"- {action}")
    
    print("\nEnding movie night:")
    for action in theater.end_movie():
        print(f"- {action}")