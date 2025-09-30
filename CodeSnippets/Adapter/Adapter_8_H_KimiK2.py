from abc import ABC, abstractmethod
import threading
import time

class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str) -> None: ...

class AudioPlayer(MediaPlayer):
    def play(self, filename: str) -> None:
        if filename.endswith(".mp3"):
            print(f"[AudioPlayer] Playing mp3: {filename}")
        else:
            raise ValueError("Unsupported format")

class VideoPlayer:
    def render_video(self, file: str) -> None:
        print(f"[VideoPlayer] Rendering video: {file}")

class VideoMediaBridge(MediaPlayer):
    def __init__(self):
        self._video_tool = VideoPlayer()
        self._lock = threading.Lock()

    def play(self, filename: str) -> None:
        if not filename.endswith((".mp4", ".mkv")):
            raise ValueError("Unsupported video format")
        with self._lock:
            time.sleep(0.01)
            self._video_tool.render_video(filename)

class PlayerFactory:
    _registry = {
        "mp3": AudioPlayer,
        "mp4": VideoMediaBridge,
        "mkv": VideoMediaBridge,
    }

    @classmethod
    def create(cls, ext: str) -> MediaPlayer:
        if ext not in cls._registry:
            raise ValueError("No suitable player")
        return cls._registry[ext]()

def main():
    files = ["song.mp3", "clip.mp4", "movie.mkv"]
    for f in files:
        ext = f.split(".")[-1]
        player = PlayerFactory.create(ext)
        player.play(f)

if __name__ == "__main__":
    main()