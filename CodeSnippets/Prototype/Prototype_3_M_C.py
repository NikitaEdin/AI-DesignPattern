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
        return f"Document(id={self.creation_id}, title='{self.title}', content_length={len(self.content)})"

class DocumentManager:
    def __init__(self):
        self.templates = {}
    
    def register_template(self, name, document):
        if not isinstance(document, Cloneable):
            raise TypeError("Document must implement Cloneable interface")
        self.templates[name] = document
    
    def create_from_template(self, template_name):
        if template_name not in self.templates:
            raise KeyError(f"Template '{template_name}' not found")
        return self.templates[template_name].clone()

if __name__ == "__main__":
    manager = DocumentManager()
    
    original_doc = Document("Report Template", "Executive Summary: [Content Here]", 
                          {"department": "Finance", "confidential": True})
    
    manager.register_template("finance_report", original_doc)
    
    doc1 = manager.create_from_template("finance_report")
    doc2 = manager.create_from_template("finance_report")
    
    doc1.update_content("Q1 Financial Results: Revenue increased by 15%")
    doc1.add_metadata("quarter", "Q1")
    
    doc2.update_content("Q2 Financial Results: Revenue increased by 8%")
    doc2.add_metadata("quarter", "Q2")
    
    print(f"Original: {original_doc}")
    print(f"Clone 1: {doc1}")
    print(f"Clone 2: {doc2}")
    print(f"Doc1 metadata: {doc1.metadata}")
    print(f"Doc2 metadata: {doc2.metadata}")