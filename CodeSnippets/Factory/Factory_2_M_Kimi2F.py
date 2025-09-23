from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def open(self) -> str:
        pass

class PdfDoc(Document):
    def open(self) -> str:
        return "Opening PDF document"

class WordDoc(Document):
    def open(self) -> str:
        return "Opening Word document"

class CsvDoc(Document):
    def open(self) -> str:
        return "Opening CSV document"

class Creator:
    _registry = {
        'pdf': PdfDoc,
        'word': WordDoc,
        'csv': CsvDoc
    }

    @classmethod
    def create(cls, ext: str) -> Document:
        ext = ext.lower()
        if ext not in cls._registry:
            raise ValueError(f"Unsupported extension: {ext}")
        return cls._registry[ext]()

if __name__ == "__main__":
    for ext in ['pdf', 'word', 'csv', 'txt']:
        try:
            doc = Creator.create(ext)
            print(doc.open())
        except ValueError as e:
            print(e)