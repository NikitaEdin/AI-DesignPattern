class Mp3Player:
    def play_mp3(self, filename):
        print(f"Playing MP3 file: {filename}")

class UniversalAudioPlayer:
    def __init__(self):
        self.player = Mp3Player()

    def play(self, audio_format, filename):
        if audio_format == "mp3":
            self.player.play_mp3(filename)
        else:
            print("Unsupported audio format")

if __name__ == "__main__":
    audio_player = UniversalAudioPlayer()
    audio_player.play("mp3", "song.mp3")
    audio_player.play("wav", "track.wav")