class AudioPlayer:
    def play(self, format_type, file_name):
        raise NotImplementedError("Subclasses must implement play method")

class Mp3Specialist(AudioPlayer):
    def play(self, format_type, file_name):
        if not isinstance(file_name, str):
            raise ValueError("File name must be a string")
        if format_type.lower() == "mp3":
            print(f"Playing MP3 file: {file_name}")
        else:
            raise ValueError(f"Unsupported format: {format_type}")

class VersatilePlayer:
    def play_wav(self, file_name):
        if not isinstance(file_name, str):
            raise ValueError("File name must be a string")
        print(f"Playing WAV file: {file_name}")

    def play_aac(self, file_name):
        if not isinstance(file_name, str):
            raise ValueError("File name must be a string")
        print(f"Playing AAC file: {file_name}")

class ComprehensiveAudioPlayer(AudioPlayer):
    def __init__(self, versatile_instance):
        if not isinstance(versatile_instance, VersatilePlayer):
            raise ValueError("Must provide a VersatilePlayer instance")
        self.versatile = versatile_instance

    def play(self, format_type, file_name):
        if not isinstance(file_name, str):
            raise ValueError("File name must be a string")
        if format_type.lower() == "wav":
            self.versatile.play_wav(file_name)
        elif format_type.lower() == "aac":
            self.versatile.play_aac(file_name)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

if __name__ == "__main__":
    mp3_unit = Mp3Specialist()
    mp3_unit.play("mp3", "track.mp3")

    versatile_unit = VersatilePlayer()
    comprehensive_unit = ComprehensiveAudioPlayer(versatile_unit)
    comprehensive_unit.play("wav", "audio.wav")
    comprehensive_unit.play("aac", "song.aac")

    try:
        comprehensive_unit.play("mp3", "invalid.mp3")
    except ValueError as e:
        print(f"Error: {e}")