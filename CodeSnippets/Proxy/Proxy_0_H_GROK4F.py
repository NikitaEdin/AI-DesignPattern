from abc import ABC, abstractmethod

class Displayable(ABC):
    @abstractmethod
    def show(self, location: str):
        pass

    @abstractmethod
    def get_dimensions(self) -> tuple[int, int]:
        pass

class HighResolutionImage(Displayable):
    def __init__(self, image_name: str):
        self.image_name = image_name
        self._load_image()

    def _load_image(self):
        print(f"Loading high-resolution image: {self.image_name} from disk")

    def show(self, location: str):
        print(f"Displaying {self.image_name} at {location}")

    def get_dimensions(self) -> tuple[int, int]:
        print(f"Retrieving dimensions from loaded image: {self.image_name}")
        return (1920, 1080)

class CachedImageHandler(Displayable):
    _metadata_cache = {}
    _loaded_images = {}

    def __init__(self, image_name: str):
        if not image_name or not isinstance(image_name, str):
            raise ValueError("Image name must be a non-empty string")
        self.image_name = image_name

    def get_dimensions(self) -> tuple[int, int]:
        if self.image_name not in self._metadata_cache:
            print(f"Fetching metadata for {self.image_name}")
            self._metadata_cache[self.image_name] = (800, 600)
        return self._metadata_cache[self.image_name]

    def show(self, location: str):
        if location is None:
            location = "default location"
        if self.image_name not in self._loaded_images:
            print(f"Instantiating full image loader for {self.image_name}")
            self._loaded_images[self.image_name] = HighResolutionImage(self.image_name)
        self._loaded_images[self.image_name].show(location)

if __name__ == "__main__":
    handler1 = CachedImageHandler("photo1.jpg")
    dims1 = handler1.get_dimensions()
    print(f"Initial dimensions for photo1: {dims1}")
    handler1.show("top-left")

    handler2 = CachedImageHandler("photo1.jpg")
    dims2 = handler2.get_dimensions()
    print(f"Cached dimensions for photo1: {dims2}")
    handler2.show("top-right")

    handler3 = CachedImageHandler("photo2.jpg")
    dims3 = handler3.get_dimensions()
    print(f"Initial dimensions for photo2: {dims3}")
    handler3.show("bottom-center")