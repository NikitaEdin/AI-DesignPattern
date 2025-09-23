class AudioSystem:
    def start_audio(self):
        print("Audio system on")
    
    def stop_audio(self):
        print("Audio system off")

class VideoSystem:
    def start_video(self):
        print("Video system on")
    
    def stop_video(self):
        print("Video system off")

class LightSystem:
    def dim_lights(self):
        print("Lights dimmed")
    
    def bright_lights(self):
        print("Lights on")

class HomeTheater:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lights = LightSystem()
    
    def watch_movie(self):
        self.lights.dim_lights()
        self.audio.start_audio()
        self.video.start_video()
    
    def end_movie(self):
        self.video.stop_video()
        self.audio.stop_audio()
        self.lights.bright_lights()

if __name__ == "__main__":
    theater = HomeTheater()
    theater.watch_movie()
    theater.end_movie()