import copy

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def clone(self):
        return copy.deepcopy(self)

    def display(self):
        print(f"{self.title}: {self.content}")

if __name__ == "__main__":
    original = Document("Report", {"pages": 10, "text": "Summary"})
    copy1 = original.clone()
    copy1.title = "Report Copy"
    copy1.content["pages"] = 5
    original.display()
    copy1.display()