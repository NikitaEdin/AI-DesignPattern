class MediaPlayer:
    def play(self, audio_type, file_name):
        raise NotImplementedError("Subclasses must implement play method")

class VlcPlayer:
    def play_vlc(self, file_name):
        print(f"Playing vlc file: {file_name}")

class Mp3Player(MediaPlayer):
    def play(self, audio_type, file_name):
        if audio_type.lower() == 'mp3':
            if file_name.lower().endswith('.mp3'):
                print(f"Playing mp3 file: {file_name}")
            else:
                raise ValueError(f"Invalid file extension for mp3: {file_name}")
        else:
            raise ValueError(f"Unsupported audio type in Mp3Player: {audio_type}")

class VlcMediaPlayer(MediaPlayer):
    def __init__(self):
        self.vlc_player = VlcPlayer()

    def play(self, audio_type, file_name):
        if audio_type.lower() == 'vlc':
            if file_name.lower().endswith('.vlc'):
                self.vlc_player.play_vlc(file_name)
            else:
                raise ValueError(f"Invalid file extension for vlc: {file_name}")
        else:
            raise ValueError(f"Unsupported audio type in VlcMediaPlayer: {audio_type}")

if __name__ == "__main__":
    mp3_player = Mp3Player()
    mp3_player.play('mp3', 'song.mp3')

    vlc_media = VlcMediaPlayer()
    vlc_media.play('vlc', 'video.vlc')

    try:
        vlc_media.play('mp3', 'song.mp3')
    except ValueError as e:
        print(f"Error: {e}")

    try:
        mp3_player.play('vlc', 'video.vlc')
    except ValueError as e:
        print(f"Error: {e}")