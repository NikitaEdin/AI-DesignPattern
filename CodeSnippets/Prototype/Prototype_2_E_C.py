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
    def __init__(self, title, content, department):
        super().__init__(title, content)
        self.department = department
    
    def __str__(self):
        return f"{self.title} ({self.department}): {self.content}"

if __name__ == "__main__":
    original = Report("Monthly Report", "Sales data", "Finance")
    copy1 = original.clone()
    copy1.title = "Weekly Report"
    copy1.content = "Updated data"
    
    print(original)
    print(copy1)