from abc import ABC, abstractmethod
import os
import threading
import time

class Image(ABC):
    @abstractmethod
    def display(self):
        pass

class BitmapImage(Image):
    def __init__(self, path):
        if not path or not isinstance(path, str):
            raise ValueError("Path must be a non-empty string")
        self.path = path
        self._data = None
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")
        print(f"Loading image from {self.path}...")
        time.sleep(1)  # Simulate expensive loading
        self._data = f"Pixel data for {self.path}"

    def display(self):
        if self._data is None:
            raise RuntimeError("Image not loaded")
        print(f"Displaying: {self._data}")

class ImageHandler(Image):
    def __init__(self, path):
        self.path = path
        self._image = None
        self._lock = threading.Lock()
        self._load_count = 0

    def display(self):
        with self._lock:
            self._load_count += 1
            if self._image is None:
                try:
                    self._image = BitmapImage(self.path)
                except (ValueError, FileNotFoundError) as e:
                    print(f"Error handling image: {e}")
                    return
            self._image.display()
            if self._load_count % 3 == 0:
                print(f"Image accessed {self._load_count} times")

    def release(self):
        with self._lock:
            self._image = None
            self._load_count = 0
            print("Image resources released")

if __name__ == "__main__":
    handler = ImageHandler("sample.jpg")
    handler.display()
    handler.display()
    handler.display()
    handler.release()
    handler.display()

    def worker(handler):
        for _ in range(2):
            handler.display()
            time.sleep(0.5)

    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(handler,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()