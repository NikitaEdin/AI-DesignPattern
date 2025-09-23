import copy
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Document(Cloneable):
    def __init__(self, title="", content="", author=""):
        self.title = title
        self.content = content
        self.author = author
        self.metadata = {}
    
    def clone(self):
        try:
            return copy.deepcopy(self)
        except Exception as e:
            raise RuntimeError(f"Failed to clone document: {e}")
    
    def set_metadata(self, key, value):
        self.metadata[key] = value
    
    def __str__(self):
        return f"Document(title='{self.title}', author='{self.author}')"

class DocumentRegistry:
    def __init__(self):
        self._templates = {}
    
    def register_template(self, name, document):
        if not isinstance(document, Cloneable):
            raise ValueError("Document must implement Cloneable interface")
        self._templates[name] = document
    
    def create_from_template(self, template_name):
        if template_name not in self._templates:
            raise KeyError(f"Template '{template_name}' not found")
        return self._templates[template_name].clone()

if __name__ == "__main__":
    registry = DocumentRegistry()
    
    report_template = Document("Monthly Report", "Report content here", "Admin")
    report_template.set_metadata("type", "report")
    report_template.set_metadata("department", "finance")
    
    registry.register_template("monthly_report", report_template)
    
    new_report = registry.create_from_template("monthly_report")
    new_report.title = "Q1 Financial Report"
    new_report.author = "John Doe"
    
    print(f"Original: {report_template}")
    print(f"Clone: {new_report}")
    print(f"Metadata preserved: {new_report.metadata}")