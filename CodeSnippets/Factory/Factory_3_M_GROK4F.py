from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def display(self):
        pass

class PDFDocument(Document):
    def display(self):
        return "Displaying PDF content"

class WordDocument(Document):
    def display(self):
        return "Displaying Word content"

class HTMLDocument(Document):
    def display(self):
        return "Displaying HTML content"

class DocumentCreator:
    @classmethod
    def create(cls, doc_type):
        if doc_type == "pdf":
            return PDFDocument()
        elif doc_type == "word":
            return WordDocument()
        elif doc_type == "html":
            return HTMLDocument()
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")

if __name__ == "__main__":
    try:
        pdf = DocumentCreator.create("pdf")
        print(pdf.display())
        
        word = DocumentCreator.create("word")
        print(word.display())
        
        html = DocumentCreator.create("html")
        print(html.display())
        
        DocumentCreator.create("txt")
    except ValueError as e:
        print(f"Error: {e}")