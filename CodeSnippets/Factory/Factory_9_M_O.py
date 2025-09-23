from abc import ABC, abstractmethod
from typing import Callable, Dict, Any

class Processor(ABC):
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

class ImageProcessor(Processor):
    def __init__(self, quality: int = 75):
        self.quality = quality
    def process(self, data: bytes) -> str:
        return f"Image processed ({len(data)} bytes) at quality {self.quality}"

class TextProcessor(Processor):
    def __init__(self, language: str = "en"):
        self.language = language
    def process(self, data: str) -> str:
        return f"Text processed ({len(data)} chars) in {self.language}"

class AudioProcessor(Processor):
    def __init__(self, bitrate: int = 128):
        self.bitrate = bitrate
    def process(self, data: bytes) -> str:
        return f"Audio processed ({len(data)} bytes) at {self.bitrate} kbps"

class ProcessorManager:
    def __init__(self):
        self._registry: Dict[str, Callable[..., Processor]] = {}
        self._cache: Dict[str, Processor] = {}
        self._counts: Dict[str, int] = {}
    def register(self, key: str, builder: Callable[..., Processor]) -> None:
        if not callable(builder):
            raise TypeError("builder must be callable")
        self._registry[key] = builder
    def create(self, key: str, reuse: bool = True, **kwargs) -> Processor:
        if reuse and key in self._cache:
            return self._cache[key]
        builder = self._registry.get(key)
        if builder is None:
            raise ValueError(f"Unknown processor type: {key}")
        instance = builder(**kwargs)
        if not isinstance(instance, Processor):
            raise TypeError("builder must return a Processor instance")
        self._counts[key] = self._counts.get(key, 0) + 1
        if reuse:
            self._cache[key] = instance
        return instance
    def creation_count(self, key: str) -> int:
        return self._counts.get(key, 0)

if __name__ == "__main__":
    manager = ProcessorManager()
    manager.register("image", lambda quality=85: ImageProcessor(quality=quality))
    manager.register("text", lambda language="en": TextProcessor(language=language))
    manager.register("audio", lambda bitrate=192: AudioProcessor(bitrate=bitrate))

    img = manager.create("image", quality=90)
    txt = manager.create("text", language="fr")
    aud = manager.create("audio", bitrate=256)

    print(img.process(b"\x89PNG\r\n\x1a\n"))
    print(txt.process("Bonjour le monde"))
    print(aud.process(b"\x00\x01\x02"))

    same_img = manager.create("image")
    print("Reused image instance:", same_img is img)
    print("Creation counts:", {k: manager.creation_count(k) for k in ("image", "text", "audio")})

    try:
        manager.create("video")
    except Exception as e:
        print("Error:", e)