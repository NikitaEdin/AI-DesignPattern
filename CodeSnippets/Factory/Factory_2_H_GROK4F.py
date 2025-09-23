from abc import ABC, abstractmethod
from enum import Enum
import logging

class OutputFormat(Enum):
    PDF = "pdf"
    HTML = "html"
    TEXT = "text"

class Document(ABC):
    def __init__(self, content: str, config: dict = None):
        self.content = content
        self.config = config or {}
        self._validate_config()

    @abstractmethod
    def _validate_config(self):
        pass

    @abstractmethod
    def render(self) -> str:
        pass

    def save(self, filename: str):
        rendered = self.render()
        with open(filename, 'w') as f:
            f.write(rendered)
        logging.info(f"Saved {filename}")

class PDFDocument(Document):
    def _validate_config(self):
        if 'font_size' not in self.config:
            raise ValueError("PDF requires 'font_size' in config")

    def render(self) -> str:
        font_size = self.config.get('font_size', 12)
        return f"PDF Content:\n{self.content}\n(Font: {font_size})"

class HTMLDocument(Document):
    def _validate_config(self):
        if 'style' not in self.config:
            self.config['style'] = 'default'

    def render(self) -> str:
        style = self.config.get('style', 'default')
        return f"<html><head><style>{style}</style></head><body>{self.content}</body></html>"

class TextDocument(Document):
    def _validate_config(self):
        pass  # No config needed

    def render(self) -> str:
        return f"TEXT Content:\n{self.content}"

class DocumentCreator:
    _registry = {
        OutputFormat.PDF: PDFDocument,
        OutputFormat.HTML: HTMLDocument,
        OutputFormat.TEXT: TextDocument
    }
    _cache = {}

    @classmethod
    def register_format(cls, format_type: OutputFormat, document_class):
        cls._registry[format_type] = document_class

    @classmethod
    def create_document(cls, format_type: OutputFormat, content: str, config: dict = None):
        if format_type not in cls._registry:
            raise ValueError(f"Unsupported format: {format_type}")
        
        cache_key = (format_type, content, tuple(sorted(config.items())) if config else None)
        if cache_key in cls._cache:
            logging.info("Using cached document")
            return cls._cache[cache_key]
        
        document_class = cls._registry[format_type]
        document = document_class(content, config)
        cls._cache[cache_key] = document
        return document

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create documents
    pdf_doc = DocumentCreator.create_document(OutputFormat.PDF, "Hello PDF", {"font_size": 14})
    pdf_doc.render()
    pdf_doc.save("output.pdf")
    
    html_doc = DocumentCreator.create_document(OutputFormat.HTML, "Hello HTML", {"style": "bold"})
    html_doc.render()
    html_doc.save("output.html")
    
    # Cache demo
    cached_pdf = DocumentCreator.create_document(OutputFormat.PDF, "Hello PDF", {"font_size": 14})
    
    # Edge case: Invalid format
    try:
        DocumentCreator.create_document("invalid", "test")
    except ValueError as e:
        logging.error(e)
    
    # Dynamic registration (advanced feature demo, though not used here)
    class CustomDocument(Document):
        def _validate_config(self):
            pass
        def render(self) -> str:
            return f"CUSTOM: {self.content}"
    
    DocumentCreator.register_format("custom", CustomDocument)