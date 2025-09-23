class ActualImage:
    def __init__(self, filename):
        self.filename = filename
        self.loaded = False

    def display(self):
        if not self.loaded:
            print(f"Loading {self.filename}")
            self.loaded = True
        print(f"Displaying {self.filename}")

class LazyImage:
    def __init__(self, filename):
        self.filename = filename
        self.actual_image = None

    def display(self):
        if self.actual_image is None:
            self.actual_image = ActualImage(self.filename)
        self.actual_image.display()

if __name__ == "__main__":
    image = LazyImage("photo.jpg")
    image.display()
    image.display()