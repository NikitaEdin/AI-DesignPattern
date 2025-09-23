from abc import ABC, abstractmethod
from typing import Dict, Type, Any, Optional
import json

class Document(ABC):
    def __init__(self, content: str = ""):
        self.content = content
        self._metadata = {}
    
    @abstractmethod
    def process(self) -> str:
        pass
    
    @abstractmethod
    def get_format(self) -> str:
        pass
    
    def add_metadata(self, key: str, value: Any):
        self._metadata[key] = value

class PDFDocument(Document):
    def process(self) -> str:
        return f"PDF: {self.content} | Metadata: {json.dumps(self._metadata)}"
    
    def get_format(self) -> str:
        return "PDF"

class WordDocument(Document):
    def process(self) -> str:
        return f"DOCX: {self.content.upper()} | Metadata: {json.dumps(self._metadata)}"
    
    def get_format(self) -> str:
        return "DOCX"

class TextDocument(Document):
    def process(self) -> str:
        return f"TXT: {self.content.strip()} | Metadata: {json.dumps(self._metadata)}"
    
    def get_format(self) -> str:
        return "TXT"

class DocumentProcessor:
    _document_types: Dict[str, Type[Document]] = {}
    _instances: Dict[str, Document] = {}
    
    @classmethod
    def register_document_type(cls, doc_type: str, document_class: Type[Document]):
        if not issubclass(document_class, Document):
            raise ValueError("Document class must inherit from Document")
        cls._document_types[doc_type.upper()] = document_class
    
    @classmethod
    def create_document(cls, doc_type: str, content: str = "", **kwargs) -> Document:
        doc_type_upper = doc_type.upper()
        if doc_type_upper not in cls._document_types:
            raise ValueError(f"Unknown document type: {doc_type}")
        
        document_class = cls._document_types[doc_type_upper]
        document = document_class(content)
        
        for key, value in kwargs.items():
            document.add_metadata(key, value)
        
        return document
    
    @classmethod
    def get_singleton_document(cls, doc_type: str, content: str = "", **kwargs) -> Document:
        cache_key = f"{doc_type.upper()}_{hash(content)}"
        if cache_key not in cls._instances:
            cls._instances[cache_key] = cls.create_document(doc_type, content, **kwargs)
        return cls._instances[cache_key]
    
    @classmethod
    def get_supported_types(cls) -> list:
        return list(cls._document_types.keys())

DocumentProcessor.register_document_type("PDF", PDFDocument)
DocumentProcessor.register_document_type("DOCX", WordDocument)
DocumentProcessor.register_document_type("TXT", TextDocument)

if __name__ == "__main__":
    doc1 = DocumentProcessor.create_document("PDF", "Sample PDF content", author="John", version=1.0)
    doc2 = DocumentProcessor.create_document("DOCX", "Word document text", title="Report")
    doc3 = DocumentProcessor.create_document("TXT", "  Plain text content  ")
    
    print(doc1.process())
    print(doc2.process())
    print(doc3.process())
    
    singleton1 = DocumentProcessor.get_singleton_document("PDF", "Cached content")
    singleton2 = DocumentProcessor.get_singleton_document("PDF", "Cached content")
    print(f"Same instance: {singleton1 is singleton2}")
    
    print(f"Supported types: {DocumentProcessor.get_supported_types()}")
    
    try:
        DocumentProcessor.create_document("INVALID", "test")
    except ValueError as e:
        print(f"Error: {e}")