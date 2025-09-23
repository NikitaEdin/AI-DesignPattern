class AudioSystem:
    def play_audio(self):
        return "Audio playing"

class VideoSystem:
    def play_video(self):
        return "Video playing"

class LightSystem:
    def dim_lights(self):
        return "Lights dimmed"

class MediaController:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lights = LightSystem()
    
    def start_movie(self):
        results = []
        results.append(self.lights.dim_lights())
        results.append(self.audio.play_audio())
        results.append(self.video.play_video())
        return results

if __name__ == "__main__":
    controller = MediaController()
    movie_setup = controller.start_movie()
    for action in movie_setup:
        print(action)