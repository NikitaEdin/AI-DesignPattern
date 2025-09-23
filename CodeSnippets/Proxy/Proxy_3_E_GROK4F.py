class ActualPicture:
    def __init__(self, filename):
        self._filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"Loading {self._filename} from disk...")

    def display(self):
        print(f"Displaying {self._filename}")

class PictureViewer:
    def __init__(self, filename):
        self._filename = filename
        self._actual_picture = None

    def display(self):
        if self._actual_picture is None:
            self._actual_picture = ActualPicture(self._filename)
        self._actual_picture.display()

if __name__ == "__main__":
    viewer = PictureViewer("image.jpg")
    viewer.display()
    viewer.display()