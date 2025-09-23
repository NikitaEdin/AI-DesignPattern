class FullImage:
    def __init__(self, filename):
        self.filename = filename
        self._load_image()

    def _load_image(self):
        try:
            print(f"Loading image from {self.filename}")
        except Exception as e:
            print(f"Error loading image: {e}")

    def display(self):
        print(f"Displaying full image: {self.filename}")

class DelayedImage:
    def __init__(self, filename):
        self.filename = filename
        self._full_image = None

    def display(self):
        if self._full_image is None:
            self._full_image = FullImage(self.filename)
        self._full_image.display()

if __name__ == "__main__":
    image1 = DelayedImage("photo1.jpg")
    image1.display()  # Triggers loading
    image1.display()  # Uses loaded instance

    print("\n" + "="*30 + "\n")

    image2 = DelayedImage("photo2.jpg")
    image2.display()  # Separate loading