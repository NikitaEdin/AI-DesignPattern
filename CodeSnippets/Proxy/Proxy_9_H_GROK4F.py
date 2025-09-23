import threading

class Document:
    def display(self):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError

class LoadedDocument(Document):
    def __init__(self, filename):
        self.filename = filename
        self.content = None
        self._load()

    def _load(self):
        try:
            if self.filename == "missing.doc":
                raise FileNotFoundError(f"{self.filename} not found")
            print(f"Loading document: {self.filename}")
            self.content = f"Full content of {self.filename} - this took time to load."
        except FileNotFoundError as e:
            print(f"Load error: {e}")
            self.content = ""

    def display(self):
        if self.content:
            print(self.content)
        else:
            print("Document could not be loaded.")

    def get_size(self):
        return len(self.content) if self.content else 0

class DocumentPlaceholder(Document):
    def __init__(self, filename):
        self.filename = filename
        self._loaded_doc = None
        self._lock = threading.Lock()
        self._error = False

    def _load_if_needed(self):
        with self._lock:
            if self._loaded_doc is None and not self._error:
                try:
                    self._loaded_doc = LoadedDocument(self.filename)
                except FileNotFoundError:
                    self._error = True

    def display(self):
        self._load_if_needed()
        if self._loaded_doc:
            self._loaded_doc.display()
        elif self._error:
            print("Unable to display: document not found.")

    def get_size(self):
        self._load_if_needed()
        if self._loaded_doc:
            return self._loaded_doc.get_size()
        elif self._error:
            return 0
        return 0

def worker(doc):
    doc.display()
    print(f"Size: {doc.get_size()}")

if __name__ == "__main__":
    valid_doc = DocumentPlaceholder("valid.doc")
    invalid_doc = DocumentPlaceholder("missing.doc")

    print("Sequential access:")
    valid_doc.display()
    valid_doc.display()  # Should not reload
    print(f"Size: {valid_doc.get_size()}")

    invalid_doc.display()
    print(f"Size: {invalid_doc.get_size()}")

    print("\nThreaded access:")
    t1 = threading.Thread(target=worker, args=(valid_doc,))
    t2 = threading.Thread(target=worker, args=(valid_doc,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()