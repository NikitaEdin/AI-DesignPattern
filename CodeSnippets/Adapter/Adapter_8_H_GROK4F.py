from typing import Union

class MediaPlayer:
    def play(self, audio_type: str, file_name: str) -> None:
        pass

class Mp3Player(MediaPlayer):
    def play(self, audio_type: str, file_name: str) -> None:
        if audio_type.lower() == 'mp3':
            print(f"Playing mp3 file: {file_name}")
        else:
            raise ValueError(f"Only mp3 supported, not {audio_type}")

class VlcPlayer:
    def play_vlc(self, file_name: str) -> None:
        print(f"Playing vlc file: {file_name}")

class Mp4Player:
    def play_mp4(self, file_name: str) -> None:
        print(f"Playing mp4 file: {file_name}")

class MediaConverter(MediaPlayer):
    def __init__(self, specific_player: Union[VlcPlayer, Mp4Player]) -> None:
        if not isinstance(specific_player, (VlcPlayer, Mp4Player)):
            raise TypeError("specific_player must be VlcPlayer or Mp4Player")
        self.specific_player = specific_player

    def play(self, audio_type: str, file_name: str) -> None:
        if not isinstance(audio_type, str) or not isinstance(file_name, str):
            raise TypeError("audio_type and file_name must be strings")
        if not audio_type.strip() or not file_name.strip():
            raise ValueError("audio_type and file_name cannot be empty")
        audio_type = audio_type.lower().strip()
        file_name = file_name.strip()
        if isinstance(self.specific_player, VlcPlayer) and audio_type == 'vlc':
            self.specific_player.play_vlc(file_name)
        elif isinstance(self.specific_player, Mp4Player) and audio_type == 'mp4':
            self.specific_player.play_mp4(file_name)
        else:
            raise ValueError(f"Incompatible format: {audio_type} for this player")

if __name__ == "__main__":
    mp3_player = Mp3Player()
    mp3_player.play("mp3", "song.mp3")
    try:
        mp3_player.play("vlc", "test.vlc")
    except ValueError as e:
        print(f"Error: {e}")
    vlc = VlcPlayer()
    converter_vlc = MediaConverter(vlc)
    converter_vlc.play("vlc", "intro.vlc")
    mp4 = Mp4Player()
    converter_mp4 = MediaConverter(mp4)
    converter_mp4.play("mp4", "alone.mp4")
    try:
        converter_vlc.play("mp4", "wrong.mp4")
    except ValueError as e:
        print(f"Error: {e}")
    try:
        converter_vlc.play("", "test.vlc")
    except ValueError as e:
        print(f"Error: {e}")
    try:
        converter_vlc.play("vlc", None)
    except TypeError as e:
        print(f"Error: {e}")