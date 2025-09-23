class AudioSystem:
    def __init__(self):
        self.volume = 50
    
    def set_volume(self, level):
        self.volume = max(0, min(100, level))
    
    def play_audio(self):
        return f"Audio playing at volume {self.volume}"

class VideoSystem:
    def __init__(self):
        self.resolution = "1080p"
    
    def set_resolution(self, res):
        self.resolution = res
    
    def start_video(self):
        return f"Video streaming in {self.resolution}"

class LightingSystem:
    def __init__(self):
        self.brightness = 100
    
    def dim_lights(self, level):
        self.brightness = max(0, min(100, level))
    
    def adjust_lighting(self):
        return f"Lights dimmed to {self.brightness}%"

class HomeTheaterController:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lighting = LightingSystem()
    
    def start_movie_mode(self):
        try:
            self.audio.set_volume(75)
            self.video.set_resolution("4K")
            self.lighting.dim_lights(20)
            
            results = [
                self.audio.play_audio(),
                self.video.start_video(),
                self.lighting.adjust_lighting()
            ]
            return "Movie mode activated: " + ", ".join(results)
        except Exception as e:
            return f"Error starting movie mode: {e}"
    
    def end_movie_mode(self):
        self.lighting.dim_lights(100)
        return "Movie mode ended, lights restored"

if __name__ == "__main__":
    theater = HomeTheaterController()
    print(theater.start_movie_mode())
    print(theater.end_movie_mode())