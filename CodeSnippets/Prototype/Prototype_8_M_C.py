import copy
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Document(Cloneable):
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.version = 1
    
    def clone(self):
        try:
            cloned = copy.deepcopy(self)
            cloned.version += 1
            return cloned
        except Exception as e:
            raise RuntimeError(f"Failed to clone document: {e}")
    
    def update_content(self, new_content):
        self.content = new_content
    
    def __str__(self):
        return f"Document(title='{self.title}', version={self.version})"

class DocumentRegistry:
    def __init__(self):
        self._templates = {}
    
    def register_template(self, name, document):
        if not isinstance(document, Cloneable):
            raise ValueError("Document must implement Cloneable interface")
        self._templates[name] = document
    
    def create_from_template(self, template_name):
        template = self._templates.get(template_name)
        if not template:
            raise KeyError(f"Template '{template_name}' not found")
        return template.clone()

if __name__ == "__main__":
    registry = DocumentRegistry()
    
    original = Document("Report Template", "Content here", {"author": "System"})
    registry.register_template("standard_report", original)
    
    doc1 = registry.create_from_template("standard_report")
    doc1.title = "Q1 Report"
    doc1.update_content("Q1 financial data")
    
    doc2 = registry.create_from_template("standard_report")
    doc2.title = "Q2 Report"
    doc2.update_content("Q2 financial data")
    
    print(f"Original: {original}")
    print(f"Clone 1: {doc1}")
    print(f"Clone 2: {doc2}")