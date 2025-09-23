import copy
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Document(Cloneable):
    def __init__(self, title, content, formatting=None):
        self.title = title
        self.content = content
        self.formatting = formatting or {}
        self.metadata = {"created": "2024-01-01", "version": 1}
    
    def clone(self):
        try:
            return copy.deepcopy(self)
        except Exception as e:
            raise RuntimeError(f"Failed to clone document: {e}")
    
    def update_content(self, new_content):
        self.content = new_content
        self.metadata["version"] += 1
    
    def __str__(self):
        return f"Document: {self.title} (v{self.metadata['version']})"

class DocumentRegistry:
    def __init__(self):
        self._templates = {}
    
    def register_template(self, name, document):
        if not isinstance(document, Cloneable):
            raise ValueError("Document must implement Cloneable interface")
        self._templates[name] = document
    
    def create_from_template(self, name):
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found")
        return self._templates[name].clone()

if __name__ == "__main__":
    registry = DocumentRegistry()
    
    report_template = Document("Monthly Report", "Template content", {"font": "Arial"})
    registry.register_template("monthly_report", report_template)
    
    january_report = registry.create_from_template("monthly_report")
    january_report.update_content("January sales data")
    january_report.title = "January Report"
    
    february_report = registry.create_from_template("monthly_report")
    february_report.update_content("February sales data")
    february_report.title = "February Report"
    
    print(january_report)
    print(february_report)
    print(f"Original template: {report_template}")