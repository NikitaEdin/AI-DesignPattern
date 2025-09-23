from abc import ABC, abstractmethod
from typing import Dict, Type, Any, Optional
import json

class Document(ABC):
    def __init__(self, content: str = ""):
        self.content = content
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        pass

class PDFDocument(Document):
    def __init__(self, content: str = "", author: str = "Unknown"):
        super().__init__(content)
        self.author = author
    
    def render(self) -> str:
        return f"PDF: {self.content[:50]}..." if len(self.content) > 50 else f"PDF: {self.content}"
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "PDF", "author": self.author, "size": len(self.content)}

class WordDocument(Document):
    def __init__(self, content: str = "", template: str = "default"):
        super().__init__(content)
        self.template = template
    
    def render(self) -> str:
        return f"DOCX[{self.template}]: {self.content}"
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "DOCX", "template": self.template, "word_count": len(self.content.split())}

class HTMLDocument(Document):
    def __init__(self, content: str = "", title: str = "Untitled"):
        super().__init__(content)
        self.title = title
    
    def render(self) -> str:
        return f"<html><title>{self.title}</title><body>{self.content}</body></html>"
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "HTML", "title": self.title, "has_content": bool(self.content)}

class DocumentCreationError(Exception):
    pass

class DocumentBuilder:
    _creators: Dict[str, Type[Document]] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def register(cls, doc_type: str, creator: Type[Document], aliases: Optional[list] = None):
        if not issubclass(creator, Document):
            raise DocumentCreationError(f"Creator must be a Document subclass")
        
        cls._creators[doc_type.lower()] = creator
        if aliases:
            for alias in aliases:
                cls._aliases[alias.lower()] = doc_type.lower()
    
    @classmethod
    def create(cls, doc_type: str, **kwargs) -> Document:
        doc_type = doc_type.lower()
        doc_type = cls._aliases.get(doc_type, doc_type)
        
        if doc_type not in cls._creators:
            available = list(cls._creators.keys()) + list(cls._aliases.keys())
            raise DocumentCreationError(f"Unknown document type '{doc_type}'. Available: {available}")
        
        try:
            return cls._creators[doc_type](**kwargs)
        except TypeError as e:
            raise DocumentCreationError(f"Invalid parameters for {doc_type}: {e}")
    
    @classmethod
    def get_available_types(cls) -> Dict[str, list]:
        return {
            "types": list(cls._creators.keys()),
            "aliases": list(cls._aliases.keys())
        }

DocumentBuilder.register("pdf", PDFDocument, ["adobe", "portable"])
DocumentBuilder.register("docx", WordDocument, ["word", "msword"])
DocumentBuilder.register("html", HTMLDocument, ["web", "htm"])

if __name__ == "__main__":
    documents = []
    
    try:
        documents.append(DocumentBuilder.create("pdf", content="Financial Report 2024", author="John Doe"))
        documents.append(DocumentBuilder.create("word", content="Meeting Notes", template="corporate"))
        documents.append(DocumentBuilder.create("html", content="Welcome to our site!", title="Homepage"))
        documents.append(DocumentBuilder.create("adobe", content="Technical Manual"))
        
        for doc in documents:
            print(f"Rendered: {doc.render()}")
            print(f"Metadata: {json.dumps(doc.get_metadata(), indent=2)}")
            print("-" * 40)
        
        print(f"Available types: {DocumentBuilder.get_available_types()}")
        
        DocumentBuilder.create("invalid", content="test")
    
    except DocumentCreationError as e:
        print(f"Error: {e}")