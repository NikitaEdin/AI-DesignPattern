import time
from abc import ABC, abstractmethod
from threading import Lock

class Graphic(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Image(Graphic):
    def __init__(self, filename: str):
        self.filename = filename
        self._load_image()

    def _load_image(self):
        time.sleep(2)

    def render(self) -> str:
        return f"Rendering {self.filename}"

class ImageGuard(Graphic):
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None
        self._lock = Lock()
        self._access_count = 0
        self._last_access = None

    def render(self) -> str:
        with self._lock:
            self._access_count += 1
            self._last_access = time.time()
            if self._real_image is None:
                self._real_image = Image(self.filename)
        return self._real_image.render()

    def stats(self) -> dict:
        return {
            "access_count": self._access_count,
            "last_access": self._last_access,
            "loaded": self._real_image is not None
        }

if __name__ == "__main__":
    guard = ImageGuard("photo.jpg")
    print(guard.stats())
    print(guard.render())
    print(guard.stats())