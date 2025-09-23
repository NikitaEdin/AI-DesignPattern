from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        pass

class PDFDocument(Document):
    def __init__(self, title: str = "Untitled"):
        self.title = title

    def render(self) -> str:
        return f"Rendering PDF: {self.title}"

    def save(self, path: str) -> None:
        print(f"Saving PDF to {path}")

class WordDocument(Document):
    def __init__(self, title: str = "Untitled"):
        self.title = title

    def render(self) -> str:
        return f"Rendering Word: {self.title}"

    def save(self, path: str) -> None:
        print(f"Saving Word to {path}")

class DocumentCreator:
    def __init__(self):
        self._registry: dict[str, type[Document]] = {}

    def register(self, doc_type: str, creator_class: type[Document]) -> None:
        self._registry[doc_type.lower()] = creator_class

    def create(self, doc_type: str, **kwargs) -> Document:
        creator_class = self._registry.get(doc_type.lower())
        if creator_class is None:
            raise ValueError(f"Unsupported document type: {doc_type}")
        return creator_class(**kwargs)

if __name__ == "__main__":
    creator = DocumentCreator()
    creator.register('pdf', PDFDocument)
    creator.register('word', WordDocument)

    try:
        pdf = creator.create('PDF', title="My Report")
        print(pdf.render())
        pdf.save("report.pdf")

        word = creator.create('WoRd', title="Notes")
        print(word.render())
        word.save("notes.doc")

        invalid = creator.create('txt')
    except ValueError as e:
        print(f"Error: {e}")

    class TXTDocument(Document):
        def __init__(self, title: str = "Untitled"):
            self.title = title

        def render(self) -> str:
            return f"Rendering TXT: {self.title}"

        def save(self, path: str) -> None:
            print(f"Saving TXT to {path}")

    creator.register('txt', TXTDocument)
    txt = creator.create('TXT', title="Log")
    print(txt.render())
    txt.save("log.txt")