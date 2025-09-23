import os

class ImageFile:
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def load(self):
        if self.data is None:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.data = f.read()
            else:
                raise FileNotFoundError(f"Image file {self.filename} not found")

    def display(self):
        self.load()
        if self.data:
            print(f"Displaying: {self.data[:50]}...")
        else:
            print("No data to display")

class ImageViewer:
    def __init__(self, filename):
        self.filename = filename
        self.image_file = None

    def display(self):
        if self.image_file is None:
            try:
                self.image_file = ImageFile(self.filename)
            except FileNotFoundError as e:
                print(e)
                return
        self.image_file.display()

if __name__ == "__main__":
    # Simulate files
    with open("sample_image.txt", "w") as f:
        f.write("This is sample image data.")
    
    viewer = ImageViewer("sample_image.txt")
    viewer.display()  # Loads and displays
    viewer.display()  # Uses cache, no reload
    
    os.remove("sample_image.txt")
    viewer.display()  # Handles error