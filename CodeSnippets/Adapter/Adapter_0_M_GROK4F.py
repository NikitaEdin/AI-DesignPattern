class MediaPlayer:
    def play(self, audio_type, file_name):
        raise NotImplementedError("Subclasses must implement play method")

class Mp3Player(MediaPlayer):
    def play(self, audio_type, file_name):
        if audio_type.lower() == "mp3":
            print(f"Playing mp3 file: {file_name}")
        else:
            print(f"Unsupported audio type: {audio_type}")

class VlcPlayer:
    def play_vlc(self, file_name):
        print(f"Playing vlc file: {file_name}")

class Mp4Player:
    def play_mp4(self, file_name):
        print(f"Playing mp4 file: {file_name}")

class VlcMediaHandler(MediaPlayer):
    def __init__(self, vlc_player):
        self.vlc_player = vlc_player

    def play(self, audio_type, file_name):
        if audio_type.lower() == "vlc":
            self.vlc_player.play_vlc(file_name)
        else:
            try:
                raise ValueError(f"Unsupported audio type for Vlc handler: {audio_type}")
            except ValueError as e:
                print(e)

class Mp4MediaHandler(MediaPlayer):
    def __init__(self, mp4_player):
        self.mp4_player = mp4_player

    def play(self, audio_type, file_name):
        if audio_type.lower() == "mp4":
            self.mp4_player.play_mp4(file_name)
        else:
            try:
                raise ValueError(f"Unsupported audio type for Mp4 handler: {audio_type}")
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    mp3_player = Mp3Player()
    mp3_player.play("mp3", "song.mp3")

    vlc_player = VlcPlayer()
    vlc_handler = VlcMediaHandler(vlc_player)
    vlc_handler.play("vlc", "video.vlc")

    mp4_player = Mp4Player()
    mp4_handler = Mp4MediaHandler(mp4_player)
    mp4_handler.play("mp4", "movie.mp4")

    vlc_handler.play("mp3", "wrong.mp3")