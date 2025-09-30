from abc import ABC, abstractmethod


class ImageInterface(ABC):

    @abstractmethod
    def display(self) -> None:
        pass


class RealImage(ImageInterface):

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._load_image()

    def _load_image(self) -> None:
        print(f"Loading image from {self.filename}...")

    def display(self) -> None:
        print(f"Displaying {self.filename}")


class CachedImage(ImageInterface):

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image = None  # type: RealImage | None

    def display(self) -> None:
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()


if __name__ == "__main__":
    img = CachedImage("example.jpg")
    img.display()
    img.display()