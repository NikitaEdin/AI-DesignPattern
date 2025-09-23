class AudioSystem:
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        return "Audio system powered on"
    
    def set_volume(self, level):
        if not self.is_on:
            raise RuntimeError("Audio system is off")
        return f"Volume set to {level}"

class VideoProjector:
    def __init__(self):
        self.is_on = False
    
    def power_on(self):
        self.is_on = True
        return "Projector powered on"
    
    def set_input(self, source):
        if not self.is_on:
            raise RuntimeError("Projector is off")
        return f"Input set to {source}"

class LightingSystem:
    def __init__(self):
        self.brightness = 100
    
    def dim_lights(self, level):
        self.brightness = level
        return f"Lights dimmed to {level}%"

class HomeTheaterController:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
    
    def start_movie(self, volume=50, input_source="HDMI"):
        try:
            results = []
            results.append(self.lights.dim_lights(20))
            results.append(self.audio.turn_on())
            results.append(self.audio.set_volume(volume))
            results.append(self.projector.power_on())
            results.append(self.projector.set_input(input_source))
            return results
        except RuntimeError as e:
            return [f"Error: {e}"]
    
    def end_movie(self):
        return [self.lights.dim_lights(100), "Systems shutting down"]

if __name__ == "__main__":
    theater = HomeTheaterController()
    
    print("Starting movie night:")
    for action in theater.start_movie():
        print(f"- {action}")
    
    print("\nEnding movie:")
    for action in theater.end_movie():
        print(f"- {action}")