class AudioPlayer:
    def play(self, audio_type, file_name):
        if audio_type == "mp3":
            print(f"Playing mp3 file: {file_name}")
        else:
            print(f"Unsupported format: {audio_type} - {file_name}")

class Mp4Player:
    def play_mp4(self, file_name):
        print(f"Playing mp4 file: {file_name}")

class Mp4Formatter:
    def __init__(self, player):
        self.player = player

    def play(self, audio_type, file_name):
        if audio_type == "mp4":
            self.player.play_mp4(file_name)
        else:
            raise ValueError(f"Unsupported format: {audio_type}")

class VlcPlayer:
    def play_vlc(self, file_name):
        print(f"Playing vlc file: {file_name}")

class VlcFormatter:
    def __init__(self, player):
        self.player = player

    def play(self, audio_type, file_name):
        if audio_type == "vlc":
            self.player.play_vlc(file_name)
        else:
            raise ValueError(f"Unsupported format: {audio_type}")

if __name__ == "__main__":
    player = AudioPlayer()
    player.play("mp3", "beyond_the_horizon.mp3")

    mp4_player = Mp4Formatter(Mp4Player())
    mp4_player.play("mp4", "alone.mp4")

    vlc_player = VlcFormatter(VlcPlayer())
    vlc_player.play("vlc", "far_far_away.vlc")

    try:
        mp4_player.play("avi", "test.avi")
    except ValueError as e:
        print(f"Error: {e}")