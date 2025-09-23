class ActualPicture:
    def __init__(self, file_path):
        self.file_path = file_path
        self._load()

    def _load(self):
        print(f"Loading picture from {self.file_path}")

    def show(self):
        print(f"Showing picture {self.file_path}")

class PictureLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self._picture = None

    def show(self):
        if self._picture is None:
            self._picture = ActualPicture(self.file_path)
        self._picture.show()

if __name__ == "__main__":
    loader1 = PictureLoader("image1.jpg")
    loader1.show()
    loader1.show()
    loader2 = PictureLoader("image2.jpg")
    loader2.show()