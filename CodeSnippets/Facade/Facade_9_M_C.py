class AudioSystem:
    def power_on(self):
        return "Audio system powered on"
    
    def set_volume(self, level):
        return f"Volume set to {level}"
    
    def power_off(self):
        return "Audio system powered off"

class VideoProjector:
    def power_on(self):
        return "Projector powered on"
    
    def set_input(self, source):
        return f"Input set to {source}"
    
    def power_off(self):
        return "Projector powered off"

class LightingSystem:
    def dim_lights(self):
        return "Lights dimmed"
    
    def bright_lights(self):
        return "Lights brightened"

class StreamingService:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True
        return "Streaming service connected"
    
    def play_movie(self, title):
        if not self.connected:
            raise RuntimeError("Service not connected")
        return f"Playing {title}"
    
    def disconnect(self):
        self.connected = False
        return "Streaming service disconnected"

class HomeTheaterManager:
    def __init__(self):
        self.audio = AudioSystem()
        self.projector = VideoProjector()
        self.lights = LightingSystem()
        self.streaming = StreamingService()
    
    def start_movie(self, title):
        results = []
        try:
            results.append(self.lights.dim_lights())
            results.append(self.audio.power_on())
            results.append(self.audio.set_volume(7))
            results.append(self.projector.power_on())
            results.append(self.projector.set_input("HDMI"))
            results.append(self.streaming.connect())
            results.append(self.streaming.play_movie(title))
            return results
        except Exception as e:
            results.append(f"Error: {str(e)}")
            return results
    
    def end_movie(self):
        results = []
        results.append(self.streaming.disconnect())
        results.append(self.projector.power_off())
        results.append(self.audio.power_off())
        results.append(self.lights.bright_lights())
        return results

if __name__ == "__main__":
    theater = HomeTheaterManager()
    
    print("Starting movie night:")
    for action in theater.start_movie("The Matrix"):
        print(f"  - {action}")
    
    print("\nEnding movie night:")
    for action in theater.end_movie():
        print(f"  - {action}")