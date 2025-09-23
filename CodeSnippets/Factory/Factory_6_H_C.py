from abc import ABC, abstractmethod
from typing import Dict, Type, Any, Optional
import json

class Document(ABC):
    def __init__(self, content: str):
        self.content = content
    
    @abstractmethod
    def process(self) -> str:
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        pass

class PDFDocument(Document):
    def process(self) -> str:
        return f"Processing PDF: {self.content[:50]}..."
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "PDF", "size": len(self.content), "pages": len(self.content) // 500 + 1}

class WordDocument(Document):
    def process(self) -> str:
        return f"Processing Word: {self.content[:50]}..."
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "DOCX", "size": len(self.content), "word_count": len(self.content.split())}

class TextDocument(Document):
    def process(self) -> str:
        return f"Processing Text: {self.content[:50]}..."
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "TXT", "size": len(self.content), "lines": self.content.count('\n') + 1}

class DocumentCreator:
    _registry: Dict[str, Type[Document]] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def register(cls, doc_type: str, document_class: Type[Document], aliases: Optional[list] = None):
        if not issubclass(document_class, Document):
            raise ValueError(f"Class {document_class.__name__} must inherit from Document")
        cls._registry[doc_type.lower()] = document_class
        if aliases:
            for alias in aliases:
                cls._aliases[alias.lower()] = doc_type.lower()
    
    @classmethod
    def create(cls, doc_type: str, content: str) -> Document:
        normalized_type = doc_type.lower()
        if normalized_type in cls._aliases:
            normalized_type = cls._aliases[normalized_type]
        
        if normalized_type not in cls._registry:
            available = list(cls._registry.keys()) + list(cls._aliases.keys())
            raise ValueError(f"Unknown document type: {doc_type}. Available: {available}")
        
        return cls._registry[normalized_type](content)
    
    @classmethod
    def get_supported_types(cls) -> Dict[str, str]:
        return {**cls._registry, **cls._aliases}

class DocumentProcessor:
    def __init__(self):
        DocumentCreator.register("pdf", PDFDocument, ["portable", "adobe"])
        DocumentCreator.register("docx", WordDocument, ["word", "doc"])
        DocumentCreator.register("txt", TextDocument, ["text", "plain"])
    
    def process_documents(self, documents_data: list) -> Dict[str, Any]:
        results = {"processed": [], "errors": [], "summary": {}}
        
        for doc_data in documents_data:
            try:
                doc_type = doc_data["type"]
                content = doc_data["content"]
                
                document = DocumentCreator.create(doc_type, content)
                processed_content = document.process()
                metadata = document.get_metadata()
                
                results["processed"].append({
                    "original_type": doc_type,
                    "processed": processed_content,
                    "metadata": metadata
                })
                
                doc_key = metadata["type"]
                results["summary"][doc_key] = results["summary"].get(doc_key, 0) + 1
                
            except Exception as e:
                results["errors"].append({"input": doc_data, "error": str(e)})
        
        return results

if __name__ == "__main__":
    processor = DocumentProcessor()
    
    test_documents = [
        {"type": "pdf", "content": "This is a PDF document with some content that needs processing"},
        {"type": "word", "content": "Word document content here with multiple words to count"},
        {"type": "txt", "content": "Plain text file\nwith multiple lines\nfor testing"},
        {"type": "adobe", "content": "Another PDF using alias"},
        {"type": "invalid", "content": "This will cause an error"}
    ]
    
    results = processor.process_documents(test_documents)
    
    print("Processing Results:")
    print(json.dumps(results, indent=2))
    
    print(f"\nSupported types: {list(DocumentCreator.get_supported_types().keys())}")