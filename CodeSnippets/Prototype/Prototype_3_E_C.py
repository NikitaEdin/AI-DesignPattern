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
    def __init__(self, title, content, data):
        super().__init__(title, content)
        self.data = data
    
    def __str__(self):
        return f"{self.title}: {self.content} (Data: {self.data})"

if __name__ == "__main__":
    original = Report("Monthly Report", "Sales data", [100, 200, 300])
    print(f"Original: {original}")
    
    copy1 = original.clone()
    copy1.title = "Weekly Report"
    copy1.data.append(400)
    
    print(f"Copy: {copy1}")
    print(f"Original after copy modification: {original}")