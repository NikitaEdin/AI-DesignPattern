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
            cloned.version = self.version + 1
            return cloned
        except Exception as e:
            raise RuntimeError(f"Failed to clone document: {e}")
    
    def update_content(self, new_content):
        self.content = new_content
    
    def __str__(self):
        return f"Document(title='{self.title}', version={self.version})"

class DocumentManager:
    def __init__(self):
        self.templates = {}
    
    def register_template(self, name, document):
        if not isinstance(document, Cloneable):
            raise ValueError("Document must implement Cloneable interface")
        self.templates[name] = document
    
    def create_from_template(self, template_name):
        if template_name not in self.templates:
            raise KeyError(f"Template '{template_name}' not found")
        return self.templates[template_name].clone()

if __name__ == "__main__":
    manager = DocumentManager()
    
    base_report = Document("Monthly Report", "Report content here", {"author": "Admin"})
    manager.register_template("report", base_report)
    
    new_report = manager.create_from_template("report")
    new_report.update_content("Updated report content")
    
    print(f"Original: {base_report}")
    print(f"Cloned: {new_report}")
    print(f"Same object: {base_report is new_report}")