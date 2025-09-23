from abc import ABC, abstractmethod

class Image(ABC):
    @abstractmethod
    def display(self):
        pass

class RealImage(Image):
    def __init__(self, filename):
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename provided")
        self._filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"Loading image: {self._filename}")

    def display(self):
        print(f"Displaying full image: {self._filename}")

class ImagePlaceholder(Image):
    def __init__(self, filename):
        self._filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            try:
                self._real_image = RealImage(self._filename)
            except ValueError as e:
                print(f"Error: {e}")
                return
        self._real_image.display()

if __name__ == "__main__":
    placeholder1 = ImagePlaceholder("image1.jpg")
    placeholder2 = ImagePlaceholder("image2.jpg")
    placeholder1.display()
    placeholder2.display()
    placeholder1.display()
    invalid_placeholder = ImagePlaceholder("")
    invalid_placeholder.display()