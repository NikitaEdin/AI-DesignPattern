import copy
from typing import Any, Dict, List

class Document:
    def __init__(self, title: str, content: str, metadata: Dict[str, Any] = None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.history: List[str] = []

    def clone(self, deep: bool = True) -> 'Document':
        new_doc = copy.deepcopy(self) if deep else copy.copy(self)
        new_doc.history = self.history.copy()
        new_doc.history.append(f"Cloned from {id(self)}")
        return new_doc

    def set_title(self, title: str) -> None:
        self.title = title
        self.history.append(f"Title changed to '{title}'")

    def set_content(self, content: str) -> None:
        self.content = content
        self.history.append(f"Content updated ({len(content)} chars)")

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value
        self.history.append(f"Metadata added: {key}={value}")

    def __repr__(self) -> str:
        return f"Document(title='{self.title}', content_length={len(self.content)}, history={len(self.history)} entries)"

class TemplateRegistry:
    def __init__(self):
        self._templates: Dict[str, Document] = {}

    def register(self, name: str, doc: Document) -> None:
        self._templates[name] = doc

    def get(self, name: str) -> Document:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found")
        return self._templates[name].clone()

    def list_templates(self) -> List[str]:
        return list(self._templates.keys())

if __name__ == "__main__":
    registry = TemplateRegistry()
    
    base_report = Document("Monthly Report", "Executive Summary:\n\n")
    base_report.add_metadata("format", "PDF")
    base_report.add_metadata("department", "Finance")
    
    registry.register("finance_report", base_report)
    
    sales_report = registry.get("finance_report")
    sales_report.set_title("Q3 Sales Report")
    sales_report.set_content("Executive Summary:\nTotal sales increased by 15%...")
    sales_report.add_metadata("department", "Sales")
    
    marketing_report = registry.get("finance_report")
    marketing_report.set_title("Marketing Campaign Report")
    marketing_report.set_content("Executive Summary:\nCampaign ROI analysis...")
    marketing_report.add_metadata("department", "Marketing")
    
    print("Base template:", base_report)
    print("Sales report:", sales_report)
    print("Marketing report:", marketing_report)
    print("\nTemplate registry contents:", registry.list_templates())