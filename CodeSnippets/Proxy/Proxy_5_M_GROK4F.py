from abc import ABC, abstractmethod

class Image(ABC):
    @abstractmethod
    def display(self):
        pass

class HighResolutionImage:
    def __init__(self, filename):
        self.filename = filename
        self._data = None

    def load(self):
        if self._data is None:
            print(f"Loading image from disk: {self.filename}")
            self._data = f"Image data for {self.filename}"
        return self._data

    def display(self):
        self.load()
        print(f"Displaying: {self._data}")

class LazyImageLoader:
    def __init__(self, filename):
        self.filename = filename
        self._image = None

    def display(self):
        if self._image is None:
            self._image = HighResolutionImage(self.filename)
        self._image.display()

if __name__ == "__main__":
    loader1 = LazyImageLoader("photo1.jpg")
    loader2 = LazyImageLoader("photo2.jpg")

    print("First display of photo1:")
    loader1.display()

    print("\nSecond display of photo1 (cached):")
    loader1.display()

    print("\nDisplay of photo2:")
    loader2.display()