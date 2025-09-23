class AudioPlayer:
    def play_audio(self):
        return "Playing audio"

class VideoPlayer:
    def play_video(self):
        return "Playing video"

class SubtitleLoader:
    def load_subtitles(self):
        return "Loading subtitles"

class MediaController:
    def __init__(self):
        self.audio = AudioPlayer()
        self.video = VideoPlayer()
        self.subtitles = SubtitleLoader()
    
    def play_movie(self):
        results = []
        results.append(self.audio.play_audio())
        results.append(self.video.play_video())
        results.append(self.subtitles.load_subtitles())
        return results

if __name__ == "__main__":
    controller = MediaController()
    output = controller.play_movie()
    for result in output:
        print(result)