import copy

class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
    
    def duplicate(self):
        try:
            return copy.deepcopy(self)
        except Exception as e:
            raise RuntimeError(f"Failed to duplicate document: {e}")
    
    def __str__(self):
        return f"Document(title='{self.title}', content='{self.content[:20]}...', metadata={self.metadata})"

class Registry:
    def __init__(self):
        self._templates = {}
    
    def register(self, name, doc):
        if not isinstance(doc, Document):
            raise TypeError("Only Document instances can be registered")
        self._templates[name] = doc
    
    def create(self, name):
        if name not in self._templates:
            raise KeyError(f"No template named '{name}'")
        return self._templates[name].duplicate()

if __name__ == "__main__":
    registry = Registry()
    
    report = Document("Monthly Report", "This is the content of the monthly report...", {"type": "report", "priority": "high"})
    letter = Document("Welcome Letter", "Dear customer, welcome to our service...", {"type": "letter", "signature": "CEO"})
    
    registry.register("standard_report", report)
    registry.register("welcome_letter", letter)
    
    new_report = registry.create("standard_report")
    new_report.title = "Q3 Report"
    new_report.metadata["priority"] = "medium"
    
    new_letter = registry.create("welcome_letter")
    new_letter.title = "Welcome John"
    
    print(report)
    print(new_report)
    print(letter)
    print(new_letter)