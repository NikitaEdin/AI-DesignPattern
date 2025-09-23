from abc import ABC, abstractmethod
import sys

class Document(ABC):
    def __init__(self, content):
        self.content = content

    @abstractmethod
    def render(self):
        pass

class TextDocument(Document):
    def render(self):
        return f"Text: {self.content}"

class ImageDocument(Document):
    def render(self):
        if not self.content.endswith(('.jpg', '.png')):
            raise ValueError("Invalid image format")
        return f"Image: {self.content}"

class PDFDocument(Document):
    def __init__(self, content):
        if not isinstance(content, dict):
            raise TypeError("PDF needs dict content")
        super().__init__(content)

    def render(self):
        return f"PDF: {self.content.get('title', 'Unknown')}"

class DocumentManager:
    _creators = {
        'text': TextDocument,
        'image': ImageDocument,
        'pdf': PDFDocument
    }

    @classmethod
    def create_document(cls, doc_type, content):
        if doc_type not in cls._creators:
            raise ValueError(f"Unknown document type: {doc_type}")
        creator = cls._creators[doc_type]
        try:
            return creator(content)
        except (ValueError, TypeError) as e:
            print(f"Error creating {doc_type}: {e}", file=sys.stderr)
            return None

    @classmethod
    def register_document_type(cls, doc_type, creator_class):
        cls._creators[doc_type] = creator_class

if __name__ == "__main__":
    doc1 = DocumentManager.create_document('text', 'Hello World')
    print(doc1.render())

    doc2 = DocumentManager.create_document('image', 'photo.jpg')
    print(doc2.render())

    doc3 = DocumentManager.create_document('pdf', {'title': 'My Doc'})
    print(doc3.render())

    doc4 = DocumentManager.create_document('image', 'notimage.txt')
    if doc4:
        print(doc4.render())
    else:
        print("Failed to create")

    try:
        doc5 = DocumentManager.create_document('unknown', 'data')
    except ValueError as e:
        print(e)