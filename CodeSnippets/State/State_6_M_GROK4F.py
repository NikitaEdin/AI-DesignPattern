from abc import ABC, abstractmethod

class ProcessMode(ABC):
    @abstractmethod
    def advance(self, processor):
        pass

    @abstractmethod
    def display_status(self):
        pass

class DraftMode(ProcessMode):
    def advance(self, processor):
        processor.current_mode = ReviewMode()

    def display_status(self):
        return "Draft"

class ReviewMode(ProcessMode):
    def advance(self, processor):
        processor.current_mode = PublishedMode()

    def display_status(self):
        return "Under Review"

class PublishedMode(ProcessMode):
    def advance(self, processor):
        raise ValueError("Cannot advance beyond published.")

    def display_status(self):
        return "Published"

class DocumentProcessor:
    def __init__(self):
        self.current_mode = DraftMode()

    def advance_process(self):
        self.current_mode.advance(self)

    def get_status(self):
        return self.current_mode.display_status()

if __name__ == "__main__":
    doc = DocumentProcessor()
    print(doc.get_status())
    doc.advance_process()
    print(doc.get_status())
    doc.advance_process()
    print(doc.get_status())
    try:
        doc.advance_process()
    except ValueError as e:
        print(e)