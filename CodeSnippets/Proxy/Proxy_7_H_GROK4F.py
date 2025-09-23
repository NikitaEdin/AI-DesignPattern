class ActualImage:
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def load(self):
        print(f"Loading {self.filename} from disk...")
        if "missing" in self.filename:
            raise FileNotFoundError(f"File {self.filename} not found")

    def show(self):
        print(f"Displaying image: {self.filename}")

class DelayedImage:
    def __init__(self, filename, access_level=1):
        self.filename = filename
        self.access_level = access_level
        self._actual_image = None

    def show(self):
        if self._actual_image is None:
            try:
                self._actual_image = ActualImage(self.filename)
            except FileNotFoundError as e:
                print(f"Load error: {e}")
                return
        if self.access_level < 3:
            print("Access denied: insufficient permissions")
            return
        self._actual_image.show()

if __name__ == "__main__":
    viewer1 = DelayedImage("photo.jpg", 5)
    viewer1.show()
    viewer1.show()

    viewer2 = DelayedImage("secret.jpg", 2)
    viewer2.show()

    viewer3 = DelayedImage("missing.jpg", 5)
    viewer3.show()