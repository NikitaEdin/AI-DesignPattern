import time
import threading

class HeavyDocumentLoader:
    def __init__(self, filename):
        self.filename = filename
        self._load(filename)

    def _load(self, filename):
        if filename.startswith("invalid"):
            raise ValueError(f"Cannot load invalid document: {filename}")
        print(f"Loading heavy document: {filename}")
        time.sleep(2)

    def display(self):
        print(f"Displaying document: {self.filename}")

class SmartDocumentLoader:
    _cache = {}
    _global_lock = threading.Lock()

    def __init__(self, filename):
        self.filename = filename

    def display(self):
        with self.__class__._global_lock:
            if self.filename not in self.__class__._cache:
                try:
                    self.__class__._cache[self.filename] = HeavyDocumentLoader(self.filename)
                except ValueError as e:
                    print(f"Failed to load {self.filename}: {e}")
                    return
            self.__class__._cache[self.filename].display()

if __name__ == "__main__":
    print("First access to shared.pdf:")
    loader1 = SmartDocumentLoader("shared.pdf")
    loader1.display()
    print("\nSecond access to same via loader1:")
    loader1.display()
    print("\nAccess via new loader2 for shared.pdf:")
    loader2 = SmartDocumentLoader("shared.pdf")
    loader2.display()
    print("\nAccess to different document:")
    loader3 = SmartDocumentLoader("report.pdf")
    loader3.display()
    print("\nThreaded access to shared.pdf:")
    def threaded_view(loader, name):
        for i in range(2):
            print(f"Thread {name} iteration {i+1}:")
            loader.display()
            time.sleep(0.5)
    threads = []
    for i in range(3):
        t = threading.Thread(target=threaded_view, args=(loader1, i))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("\nAccess to invalid document:")
    loader4 = SmartDocumentLoader("invalid.doc")
    loader4.display()