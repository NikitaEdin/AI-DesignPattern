from abc import ABC, abstractmethod
from enum import Enum
import json

class DocumentType(Enum):
    REPORT = "report"
    MEMO = "memo"
    LETTER = "letter"

class Document(ABC):
    def __init__(self, title: str):
        self.title = title
        self.content = []

    @abstractmethod
    def generate_content(self):
        pass

    def add_paragraph(self, text: str):
        self.content.append(text)

    def save(self, format_type: str = "json") -> str:
        if format_type == "json":
            data = {
                "title": self.title,
                "content": self.content,
                "type": self.__class__.__name__.lower()
            }
            return json.dumps(data, indent=2)
        raise ValueError(f"Unsupported format: {format_type}")

class ReportDocument(Document):
    def generate_content(self):
        self.add_paragraph(f"Executive Summary for {self.title}")
        self.add_paragraph("Detailed analysis follows.")
        self.add_paragraph("Recommendations:")

class MemoDocument(Document):
    def generate_content(self):
        self.add_paragraph(f"Memorandum: {self.title}")
        self.add_paragraph("To: All Staff")
        self.add_paragraph("Purpose: Informational update.")

class LetterDocument(Document):
    def generate_content(self):
        self.add_paragraph(f"Dear Recipient,")
        self.add_paragraph(f"Regarding {self.title},")
        self.add_paragraph("Sincerely,")

class DocumentCreator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_document(self, doc_type: str, title: str) -> Document:
        doc_type = doc_type.lower()
        if doc_type == DocumentType.REPORT.value:
            return ReportDocument(title)
        elif doc_type == DocumentType.MEMO.value:
            return MemoDocument(title)
        elif doc_type == DocumentType.LETTER.value:
            return LetterDocument(title)
        else:
            raise ValueError(f"Unknown document type: {doc_type}")

def main():
    creator = DocumentCreator()
    
    try:
        report = creator.create_document("report", "Annual Financial Review")
        report.generate_content()
        print("Report saved:")
        print(report.save())
        print("\n" + "="*50 + "\n")
        
        memo = creator.create_document("memo", "Policy Update")
        memo.generate_content()
        print("Memo saved:")
        print(memo.save())
        print("\n" + "="*50 + "\n")
        
        letter = creator.create_document("letter", "Invitation to Conference")
        letter.generate_content()
        print("Letter saved:")
        print(letter.save())
        
        # Edge case: invalid type
        creator.create_document("invalid", "Test")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()