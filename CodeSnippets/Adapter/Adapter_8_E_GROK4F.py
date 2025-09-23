class MediaPlayer:
    def play(self, audio_type, file_name):
        pass

class VlcPlayer:
    def vlc_play(self, file_name):
        print(f"Playing vlc file: {file_name}")

class VlcMediaPlayer(MediaPlayer):
    def __init__(self):
        self.vlc_player = VlcPlayer()

    def play(self, audio_type, file_name):
        if audio_type == "vlc":
            self.vlc_player.vlc_play(file_name)
        else:
            print("Invalid media. Only vlc supported.")

if __name__ == "__main__":
    player = VlcMediaPlayer()
    player.play("vlc", "movie.vlc")