from abc import ABC, abstractmethod
from typing import ClassVar, Dict, Optional
import time

class Image(ABC):
    @abstractmethod
    def show(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

class ActualImage(Image):
    def __init__(self, filename: str):
        print(f"Loading actual image: {filename}")
        time.sleep(1)
        if "faulty" in filename:
            raise RuntimeError("Failed to load image due to corruption.")
        self._content = f"High-resolution image: {filename}"

    def show(self) -> str:
        return self._content

    def get_size(self) -> int:
        return len(self._content)

class ImageManager(Image):
    VALID_FILES: ClassVar[set[str]] = {"image1.jpg", "faulty.jpg"}
    AUTHORIZED_USERS: ClassVar[set[str]] = {"admin"}
    _image_cache: ClassVar[Dict[str, Optional[ActualImage]]] = {}

    def __init__(self, filename: str, user: str):
        self._filename = filename
        self._user = user

    def show(self) -> str:
        if self._user not in ImageManager.AUTHORIZED_USERS:
            return "Access denied."
        if self._filename not in ImageManager.VALID_FILES:
            return "File not found."
        if self._filename not in ImageManager._image_cache:
            try:
                ImageManager._image_cache[self._filename] = ActualImage(self._filename)
            except Exception as e:
                ImageManager._image_cache[self._filename] = None
                return f"Error loading image: {str(e)}"
        if ImageManager._image_cache[self._filename] is None:
            return "Image load previously failed."
        return ImageManager._image_cache[self._filename].show()

    def get_size(self) -> int:
        if self._user not in ImageManager.AUTHORIZED_USERS:
            return 0
        if self._filename not in ImageManager.VALID_FILES:
            return 0
        if self._filename not in ImageManager._image_cache:
            try:
                ImageManager._image_cache[self._filename] = ActualImage(self._filename)
            except Exception:
                ImageManager._image_cache[self._filename] = None
                return 0
        if ImageManager._image_cache[self._filename] is None:
            return 0
        return ImageManager._image_cache[self._filename].get_size()

if __name__ == "__main__":
    img1 = ImageManager("image1.jpg", "admin")
    print(img1.show())
    print(img1.get_size())
    img2 = ImageManager("image1.jpg", "admin")
    print(img2.show())
    print(img2.get_size())
    img3 = ImageManager("fake.jpg", "admin")
    print(img3.show())
    img4 = ImageManager("image1.jpg", "guest")
    print(img4.show())
    img5 = ImageManager("faulty.jpg", "admin")
    print(img5.show())
    img6 = ImageManager("faulty.jpg", "admin")
    print(img6.show())