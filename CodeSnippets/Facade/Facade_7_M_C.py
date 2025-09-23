class AudioSystem:
    def turn_on(self):
        return "Audio system powered on"
    
    def set_volume(self, level):
        return f"Volume set to {level}"

class VideoProjector:
    def turn_on(self):
        return "Projector powered on"
    
    def set_input(self, source):
        return f"Input set to {source}"

class LightingSystem:
    def dim_lights(self):
        return "Lights dimmed"
    
    def turn_off(self):
        return "Lights turned off"

class ScreenController:
    def lower_screen(self):
        return "Screen lowered"
    
    def raise_screen(self):
        return "Screen raised"

class HomeTheaterManager:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
        self.screen = ScreenController()
        self.is_movie_mode = False
    
    def start_movie(self, volume_level=50):
        if self.is_movie_mode:
            return "Movie mode already active"
        
        actions = []
        actions.append(self.lights.dim_lights())
        actions.append(self.screen.lower_screen())
        actions.append(self.projector.turn_on())
        actions.append(self.projector.set_input("HDMI"))
        actions.append(self.audio.turn_on())
        actions.append(self.audio.set_volume(volume_level))
        
        self.is_movie_mode = True
        return "Movie started: " + " | ".join(actions)
    
    def end_movie(self):
        if not self.is_movie_mode:
            return "No movie currently playing"
        
        actions = []
        actions.append(self.screen.raise_screen())
        actions.append(self.lights.turn_off())
        
        self.is_movie_mode = False
        return "Movie ended: " + " | ".join(actions)

if __name__ == "__main__":
    theater = HomeTheaterManager()
    print(theater.start_movie(75))
    print(theater.end_movie())