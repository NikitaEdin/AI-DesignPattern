from abc import ABC, abstractmethod

class Image(ABC):
    @abstractmethod
    def display(self):
        pass

class RealImage:
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        print(f"Loading {self.filename} from disk")

    def display(self):
        print(f"Displaying {self.filename}")

class ImageManager(Image):
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
        self.real_image.display()

if __name__ == "__main__":
    manager1 = ImageManager("photo1.jpg")
    manager2 = ImageManager("photo2.jpg")

    print("Initial displays:")
    manager1.display()
    manager2.display()

    print("\nSubsequent displays:")
    manager1.display()
    manager2.display()