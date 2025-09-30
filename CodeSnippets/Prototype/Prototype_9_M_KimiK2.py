import copy

class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"Document(title='{self.title}', content_length={len(self.content)}, metadata={self.metadata})"

class TemplateManager:
    def __init__(self):
        self._templates = {}
    
    def add_template(self, name, document):
        self._templates[name] = document
    
    def create_from_template(self, name, **kwargs):
        if name not in self._templates:
            raise ValueError(f"Template '{name}' not found")
        
        new_doc = self._templates[name].clone()
        
        for key, value in kwargs.items():
            if hasattr(new_doc, key):
                setattr(new_doc, key, value)
        
        return new_doc

if __name__ == "__main__":
    manager = TemplateManager()
    
    original = Document("Original Report", "This is the original content.", {"author": "John", "version": 1})
    manager.add_template("report", original)
    
    duplicate = manager.create_from_template("report", title="Duplicate Report", content="Modified content")
    
    print("Original:", original)
    print("Duplicate:", duplicate)
    print("Are they different objects?", original is not duplicate)