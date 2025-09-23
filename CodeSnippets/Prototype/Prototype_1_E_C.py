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
    print(f"Original: {original}")
    
    copy1 = original.clone()
    copy1.title = "Quarterly Report"
    copy1.content = "Updated sales data"
    print(f"Copy: {copy1}")