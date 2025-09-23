class MediaPlayer:
    def play(self, audio_type, file_name):
        pass

class Mp3Player(MediaPlayer):
    def play(self, audio_type, file_name):
        if audio_type == "mp3":
            print(f"Playing mp3 file {file_name}")

class AdvancedMediaPlayer:
    def play_vlc(self, file_name):
        print(f"Playing vlc file {file_name}")

    def play_mp4(self, file_name):
        print(f"Playing mp4 file {file_name}")

class VlcMediaHandler(MediaPlayer):
    def __init__(self):
        self.advanced_player = AdvancedMediaPlayer()

    def play(self, audio_type, file_name):
        if audio_type == "vlc":
            self.advanced_player.play_vlc(file_name)

if __name__ == "__main__":
    mp3_handler = Mp3Player()
    mp3_handler.play("mp3", "song.mp3")

    vlc_handler = VlcMediaHandler()
    vlc_handler.play("vlc", "movie.mkv")