import copy

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def clone(self):
        return copy.deepcopy(self)
    
    def display(self):
        print(f"Title: {self.title}, Content: {self.content}")

class DocumentManager:
    def __init__(self):
        self.templates = {}
    
    def register_template(self, name, template):
        self.templates[name] = template
    
    def create_document(self, name):
        return self.templates[name].clone()

if __name__ == "__main__":
    manager = DocumentManager()
    
    original = Document("Template", "Default content")
    manager.register_template("basic", original)
    
    doc1 = manager.create_document("basic")
    doc1.title = "Report 1"
    
    doc2 = manager.create_document("basic")
    doc2.title = "Report 2"
    
    doc1.display()
    doc2.display()