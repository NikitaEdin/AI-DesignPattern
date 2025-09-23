from abc import ABC, abstractmethod
from typing import Type, Dict, Optional


class Document(ABC):
    def __init__(self, content: str):
        self.content = content

    @abstractmethod
    def save(self, path: str) -> None:
        pass

    def summary(self) -> str:
        return f"{self.__class__.__name__}: {self.content[:30]}"


class PdfDocument(Document):
    def save(self, path: str) -> None:
        if not path.endswith(".pdf"):
            path += ".pdf"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"PDF_CONTENT\n{self.content}")


class WordDocument(Document):
    def save(self, path: str) -> None:
        if not path.endswith(".docx"):
            path += ".docx"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"DOCX_CONTENT\n{self.content}")


class HtmlDocument(Document):
    def save(self, path: str) -> None:
        if not path.endswith(".html"):
            path += ".html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"<html><body>{self.content}</body></html>")


class DocumentCreator:
    def __init__(self):
        self._registry: Dict[str, Type[Document]] = {}
        self._cache: Dict[str, Document] = {}

    def register(self, doc_type: str, constructor: Type[Document]) -> None:
        if not issubclass(constructor, Document):
            raise TypeError("constructor must be a Document subclass")
        self._registry[doc_type.lower()] = constructor

    def create_document(self, doc_type: str, content: str, reuse: bool = False) -> Document:
        key = doc_type.lower()
        if reuse and key in self._cache:
            return self._cache[key]
        constructor = self._registry.get(key)
        if constructor is None:
            raise ValueError(f"Unknown document type: {doc_type}")
        instance = constructor(content)
        if reuse:
            self._cache[key] = instance
        return instance


def main():
    maker = DocumentCreator()
    maker.register("pdf", PdfDocument)
    maker.register("word", WordDocument)
    maker.register("html", HtmlDocument)

    try:
        doc1 = maker.create_document("pdf", "Report Q3 data and analysis", reuse=False)
        doc1.save("report_q3")
        print(doc1.summary())

        doc2 = maker.create_document("word", "Meeting notes and action items", reuse=True)
        doc2.save("meeting_notes")
        print(doc2.summary())

        doc3 = maker.create_document("word", "This content will be ignored if reused", reuse=True)
        print("Reused same instance:", doc3 is doc2)
        doc3.save("meeting_notes_reuse")

        doc4 = maker.create_document("md", "Markdown content", reuse=False)
        doc4.save("notes")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()