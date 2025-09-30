import copy
from typing import Any, Dict

class DocumentTemplate:
    def __init__(self, title: str, content: str, metadata: Dict[str, Any] = None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}

    def clone(self) -> 'DocumentTemplate':
        new_doc = copy.deepcopy(self)
        new_doc.metadata = copy.deepcopy(self.metadata)
        return new_doc

    def customize(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            elif key in self.metadata:
                self.metadata[key] = value
            else:
                raise ValueError(f"Unknown attribute: {key}")

class ReportFactory:
    def __init__(self):
        self._templates = {}

    def register_template(self, name: str, template: DocumentTemplate):
        self._templates[name] = template

    def create_report(self, template_name: str, **customizations) -> DocumentTemplate:
        if template_name not in self._templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        new_report = self._templates[template_name].clone()
        new_report.customize(**customizations)
        return new_report

if __name__ == "__main__":
    factory = ReportFactory()
    
    quarterly_template = DocumentTemplate(
        title="Quarterly Report - Q1 2024",
        content="This report covers the financial performance...",
        metadata={"type": "quarterly", "department": "finance"}
    )
    
    factory.register_template("quarterly", quarterly_template)
    
    q2_report = factory.create_report(
        "quarterly",
        title="Quarterly Report - Q2 2024",
        content="This report covers the financial performance for Q2 2024...",
        department="marketing"
    )
    
    print(f"Original: {quarterly_template.title}")
    print(f"Cloned: {q2_report.title}")
    print(f"Metadata: {q2_report.metadata}")