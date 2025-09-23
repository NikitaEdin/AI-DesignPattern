import copy

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content if isinstance(content, list) else []

    def replicate(self):
        raise NotImplementedError("Subclasses must implement replicate")

    def display(self):
        print(f"Title: {self.title}")
        print(f"Content: {self.content}")

class Report(Document):
    def __init__(self, title, sections, author):
        super().__init__(title, sections)
        self.author = author

    def replicate(self):
        cloned = Report(self.title, copy.deepcopy(self.content), self.author)
        return cloned

class TechnicalReport(Report):
    def __init__(self, title, sections, author, diagrams):
        super().__init__(title, sections, author)
        self.diagrams = diagrams if isinstance(diagrams, list) else []

    def replicate(self):
        cloned = TechnicalReport(
            self.title,
            copy.deepcopy(self.content),
            self.author,
            copy.deepcopy(self.diagrams)
        )
        return cloned

    def display(self):
        super().display()
        print(f"Diagrams: {self.diagrams}")

if __name__ == "__main__":
    original_report = TechnicalReport(
        "Annual Summary",
        ["Introduction", "Results"],
        "Jane Doe",
        ["chart1.png", "graph2.png"]
    )
    print("Original Report:")
    original_report.display()

    try:
        cloned_report = original_report.replicate()
        cloned_report.content.append("Conclusion")
        cloned_report.diagrams.append("new_diagram.png")
        cloned_report.title = "Cloned Annual Summary"

        print("\nCloned Report (modified):")
        cloned_report.display()

        print("\nOriginal Report (unchanged):")
        original_report.display()
    except Exception as e:
        print(f"Error during replication: {e}")