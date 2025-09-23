import abc
from typing import Protocol, runtime_checkable

@runtime_checkable
class MediaPlayer(Protocol):
    def play(self, filename: str) -> None: ...

class AudioPlayer:
    def play_audio(self, file: str) -> None:
        print(f"Playing audio: {file}")

class VideoPlayer:
    def play_video(self, file: str) -> None:
        print(f"Playing video: {file}")

class StreamingService:
    def stream(self, url: str) -> None:
        print(f"Streaming from: {url}")

class AudioBridge:
    def __init__(self, player: AudioPlayer):
        self._player = player
    def play(self, filename: str) -> None:
        if not filename.endswith(('.mp3', '.wav', '.flac')):
            raise ValueError("Unsupported audio format")
        self._player.play_audio(filename)

class VideoBridge:
    def __init__(self, player: VideoPlayer):
        self._player = player
    def play(self, filename: str) -> None:
        if not filename.endswith(('.mp4', '.mkv', '.avi')):
            raise ValueError("Unsupported video format")
        self._player.play_video(filename)

class StreamBridge:
    def __init__(self, service: StreamingService):
        self._service = service
    def play(self, url: str) -> None:
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL")
        self._service.stream(url)

class UniversalPlayer:
    def __init__(self):
        self._backends: dict[str, MediaPlayer] = {}
    def register(self, ext: str, backend: MediaPlayer) -> None:
        self._backends[ext] = backend
    def play(self, resource: str) -> None:
        ext = resource.split('.')[-1] if '.' in resource else 'stream'
        if ext not in self._backends:
            raise RuntimeError(f"No backend for {ext}")
        self._backends[ext].play(resource)

if __name__ == "__main__":
    player = UniversalPlayer()
    player.register('mp3', AudioBridge(AudioPlayer()))
    player.register('mp4', VideoBridge(VideoPlayer()))
    player.register('stream', StreamBridge(StreamingService()))
    player.play('song.mp3')
    player.play('movie.mp4')
    player.play('https://example.com/live')