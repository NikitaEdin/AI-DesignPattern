class RealImage:
    def __init__(self, url):
        self.url = url

    def load(self):
        print("Loading " + self.url)

    def display(self):
        print("Displaying " + self.url)

class ProxyImage:
    def __init__(self, url):
        self.real_image = RealImage(url)

    def load(self):
        self.real_image.load()

    def display(self):
        if not self.real_image.is_loaded():
            self.real_image.load()
        self.real_image.display()

    def is_loaded(self):
        return hasattr(self, "real_image") and self.real_image.is_loaded()

if __name__ == "__main__":
    proxy = ProxyImage("https://i.imgur.com/sM0Jg9B.jpg")
    proxy.display()