from abc import ABC, abstractmethod

class MediaPlayer(ABC):
    @abstractmethod
    def play(self, format_type: str, filename: str):
        pass

class LegacyAudioPlayer:
    def play_wav(self, filename: str):
        print(f"Playing WAV file: {filename} using legacy system.")

    def play_aiff(self, filename: str):
        print(f"Playing AIFF file: {filename} using legacy system.")

class WavPlayer(MediaPlayer):
    def __init__(self):
        self.legacy_player = LegacyAudioPlayer()

    def play(self, format_type: str, filename: str):
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename provided.")
        if format_type.lower() == 'wav':
            self.legacy_player.play_wav(filename)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

class AiffPlayer(MediaPlayer):
    def __init__(self):
        self.legacy_player = LegacyAudioPlayer()

    def play(self, format_type: str, filename: str):
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename provided.")
        if format_type.lower() == 'aiff':
            self.legacy_player.play_aiff(filename)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

if __name__ == "__main__":
    wav_player = WavPlayer()
    wav_player.play("wav", "sample.wav")

    try:
        wav_player.play("mp3", "sample.mp3")
    except ValueError as e:
        print(f"Error: {e}")

    aiff_player = AiffPlayer()
    aiff_player.play("aiff", "melody.aiff")

    try:
        aiff_player.play("wav", "wrong.wav")
    except ValueError as e:
        print(f"Error: {e}")