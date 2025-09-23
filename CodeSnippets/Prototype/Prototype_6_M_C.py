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
        self.creation_id = id(self)
    
    def clone(self):
        try:
            cloned = copy.deepcopy(self)
            cloned.creation_id = id(cloned)
            return cloned
        except Exception as e:
            raise RuntimeError(f"Failed to clone document: {e}")
    
    def update_content(self, new_content):
        self.content = new_content
    
    def add_metadata(self, key, value):
        self.metadata[key] = value
    
    def __str__(self):
        return f"Document(title='{self.title}', id={self.creation_id})"

class DocumentManager:
    def __init__(self):
        self.templates = {}
    
    def register_template(self, name, document):
        if not isinstance(document, Cloneable):
            raise ValueError("Document must be cloneable")
        self.templates[name] = document
    
    def create_from_template(self, template_name):
        if template_name not in self.templates:
            raise KeyError(f"Template '{template_name}' not found")
        return self.templates[template_name].clone()

if __name__ == "__main__":
    manager = DocumentManager()
    
    base_report = Document("Monthly Report", "Template content", {"type": "report", "version": "1.0"})
    manager.register_template("monthly_report", base_report)
    
    report1 = manager.create_from_template("monthly_report")
    report1.update_content("January sales data")
    report1.add_metadata("month", "January")
    
    report2 = manager.create_from_template("monthly_report")
    report2.update_content("February sales data")
    report2.add_metadata("month", "February")
    
    print(f"Original: {base_report}")
    print(f"Clone 1: {report1}")
    print(f"Clone 2: {report2}")
    print(f"Independent objects: {report1.creation_id != report2.creation_id}")