class AudioSystem:
    def __init__(self):
        self.volume = 50
    
    def turn_on(self):
        return "Audio system powered on"
    
    def set_volume(self, level):
        self.volume = max(0, min(100, level))
        return f"Volume set to {self.volume}"

class VideoProjector:
    def __init__(self):
        self.brightness = 75
    
    def power_on(self):
        return "Projector powered on"
    
    def set_input(self, source):
        return f"Input set to {source}"

class LightingSystem:
    def __init__(self):
        self.brightness = 100
    
    def dim_lights(self, level):
        self.brightness = max(0, min(100, level))
        return f"Lights dimmed to {self.brightness}%"

class HomeTheaterController:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
        self.is_movie_mode = False
    
    def start_movie(self, volume_level=70):
        if self.is_movie_mode:
            return "Movie mode already active"
        
        results = []
        results.append(self.lights.dim_lights(20))
        results.append(self.audio.turn_on())
        results.append(self.audio.set_volume(volume_level))
        results.append(self.projector.power_on())
        results.append(self.projector.set_input("Blu-ray"))
        
        self.is_movie_mode = True
        return "Movie mode activated: " + " | ".join(results)
    
    def end_movie(self):
        if not self.is_movie_mode:
            return "Movie mode not active"
        
        self.lights.dim_lights(100)
        self.is_movie_mode = False
        return "Movie mode deactivated: Lights restored to full brightness"

if __name__ == "__main__":
    theater = HomeTheaterController()
    
    print(theater.start_movie(80))
    print(theater.end_movie())
    print(theater.end_movie())