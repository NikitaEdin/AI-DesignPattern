class Document:
    def export(self):
        raise NotImplementedError

class PdfDocument(Document):
    def export(self):
        return "PDF: exported as .pdf"

class WordDocument(Document):
    def export(self):
        return "DOCX: exported as .docx"

class MarkdownDocument(Document):
    def export(self):
        return "MD: exported as .md"

class DocumentCreator:
    _registry = {
        "pdf": PdfDocument,
        "docx": WordDocument,
        "md": MarkdownDocument
    }

    @classmethod
    def create(cls, kind: str) -> Document:
        try:
            return cls._registry[kind.lower()]()
        except KeyError:
            raise ValueError(f"Unsupported kind: {kind}")

if __name__ == "__main__":
    for key in ("pdf", "docx", "md"):
        doc = DocumentCreator.create(key)
        print(doc.export())