import copy

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.title}: {self.content}"

class Report(Document):
    def __init__(self, title, content, author):
        super().__init__(title, content)
        self.author = author
    
    def __str__(self):
        return f"{self.title} by {self.author}: {self.content}"

if __name__ == "__main__":
    original = Report("Sales Report", "Q1 data", "John")
    copy1 = original.clone()
    copy1.title = "Marketing Report"
    copy1.author = "Jane"
    
    print(original)
    print(copy1)