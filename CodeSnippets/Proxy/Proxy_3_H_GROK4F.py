from abc import ABC, abstractmethod
import time

class ImageViewer(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def show(self):
        pass

class ResourceIntensiveViewer(ImageViewer):
    def __init__(self, image_path):
        self.image_path = image_path
        self.content = None

    def initialize(self):
        if self.content is not None:
            return
        print(f"Starting intensive processing for {self.image_path}...")
        time.sleep(2)
        if "invalid" in self.image_path:
            raise ValueError("Invalid image path")
        self.content = f"High-resolution image data from {self.image_path}"
        print("Processing complete.")

    def show(self):
        self.initialize()
        print(f"Rendering: {self.content}")

class DelayedAccessViewer(ImageViewer):
    def __init__(self, image_path, authorized=True):
        self.image_path = image_path
        self.authorized = authorized
        self.real_viewer = None
        self.cached_content = None

    def initialize(self):
        if not self.authorized:
            raise PermissionError(f"Access denied for {self.image_path}")
        if self.cached_content is not None:
            return
        if self.real_viewer is None:
            print(f"Instantiating resource-intensive viewer for {self.image_path}")
            self.real_viewer = ResourceIntensiveViewer(self.image_path)
        try:
            self.real_viewer.initialize()
            self.cached_content = self.real_viewer.content
        except ValueError as e:
            print(f"Encountered error: {e}")
            self.cached_content = "Image loading failed: invalid path provided"

    def show(self):
        try:
            if self.cached_content is None:
                self.initialize()
            print(f"Displaying: {self.cached_content}")
        except PermissionError as e:
            print(f"Display blocked: {e}")

if __name__ == "__main__":
    print("Authorized lazy loading demo:")
    handler = DelayedAccessViewer("photo.jpg", authorized=True)
    handler.show()
    handler.show()
    print("\nUnauthorized access demo:")
    try:
        restricted = DelayedAccessViewer("secure.jpg", authorized=False)
        restricted.show()
    except PermissionError as e:
        print(e)
    print("\nError handling demo:")
    faulty = DelayedAccessViewer("invalid.jpg", authorized=True)
    faulty.show()