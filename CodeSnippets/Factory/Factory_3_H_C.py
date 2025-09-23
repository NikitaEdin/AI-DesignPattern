from abc import ABC, abstractmethod
from typing import Dict, Type, Any
import json

class Document(ABC):
    def __init__(self, content: str):
        self.content = content
        self._metadata = {}
    
    @abstractmethod
    def process(self) -> str:
        pass
    
    @abstractmethod
    def get_format(self) -> str:
        pass

class PDFDocument(Document):
    def process(self) -> str:
        return f"PDF: {self.content} [compressed]"
    
    def get_format(self) -> str:
        return "pdf"

class WordDocument(Document):
    def process(self) -> str:
        return f"DOCX: {self.content} [formatted]"
    
    def get_format(self) -> str:
        return "docx"

class TextDocument(Document):
    def process(self) -> str:
        return f"TXT: {self.content} [plain]"
    
    def get_format(self) -> str:
        return "txt"

class DocumentCreator:
    _registry: Dict[str, Type[Document]] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def register(cls, doc_type: str, doc_class: Type[Document], aliases: list = None):
        if not issubclass(doc_class, Document):
            raise ValueError("Class must inherit from Document")
        cls._registry[doc_type.lower()] = doc_class
        if aliases:
            for alias in aliases:
                cls._aliases[alias.lower()] = doc_type.lower()
    
    @classmethod
    def create(cls, doc_type: str, content: str, **kwargs) -> Document:
        doc_type = doc_type.lower()
        
        if doc_type in cls._aliases:
            doc_type = cls._aliases[doc_type]
        
        if doc_type not in cls._registry:
            available = list(cls._registry.keys()) + list(cls._aliases.keys())
            raise ValueError(f"Unknown document type: {doc_type}. Available: {available}")
        
        return cls._registry[doc_type](content, **kwargs)
    
    @classmethod
    def get_supported_types(cls) -> Dict[str, str]:
        return {k: v.__name__ for k, v in cls._registry.items()}

class AdvancedDocumentProcessor:
    def __init__(self):
        self.creator = DocumentCreator()
        self._setup_default_types()
    
    def _setup_default_types(self):
        self.creator.register("pdf", PDFDocument, ["adobe", "portable"])
        self.creator.register("docx", WordDocument, ["word", "doc"])
        self.creator.register("txt", TextDocument, ["text", "plain"])
    
    def process_batch(self, documents_config: str) -> list:
        config = json.loads(documents_config)
        results = []
        
        for doc_config in config:
            try:
                doc = self.creator.create(
                    doc_config["type"], 
                    doc_config["content"]
                )
                results.append({
                    "format": doc.get_format(),
                    "processed": doc.process(),
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "error": str(e),
                    "status": "failed",
                    "input": doc_config
                })
        
        return results

if __name__ == "__main__":
    processor = AdvancedDocumentProcessor()
    
    print("Supported types:", processor.creator.get_supported_types())
    
    single_doc = processor.creator.create("pdf", "Sample document content")
    print(f"Single document: {single_doc.process()}")
    
    alias_doc = processor.creator.create("word", "Report content")
    print(f"Using alias: {alias_doc.process()}")
    
    batch_config = '''[
        {"type": "pdf", "content": "Annual report"},
        {"type": "text", "content": "Meeting notes"},
        {"type": "invalid", "content": "Test"}
    ]'''
    
    results = processor.process_batch(batch_config)
    print("\nBatch processing results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")