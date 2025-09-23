class MediaPlayer:
    def play(self, audio_type, file_name):
        pass

class BasicMediaPlayer(MediaPlayer):
    def play(self, audio_type, file_name):
        if audio_type.lower() == 'mp3':
            self._play_mp3(file_name)
        else:
            raise ValueError(f"Unsupported audio type: {audio_type}")

    def _play_mp3(self, file_name):
        print(f"Playing MP3 file: {file_name}")

class Mp4Player:
    def play_mp4(self, file_name):
        print(f"Playing MP4 file: {file_name}")

class Mp4MediaPlayer(MediaPlayer):
    def __init__(self):
        self.mp4_player = Mp4Player()

    def play(self, audio_type, file_name):
        if audio_type.lower() == 'mp4':
            self.mp4_player.play_mp4(file_name)
        else:
            raise ValueError(f"Unsupported audio type: {audio_type}")

def main():
    mp3_player = BasicMediaPlayer()
    mp3_player.play('mp3', 'song.mp3')

    mp4_player = Mp4MediaPlayer()
    mp4_player.play('mp4', 'video.mp4')

    try:
        mp3_player.play('mp4', 'video.mp4')
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()