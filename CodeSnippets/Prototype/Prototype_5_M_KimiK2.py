import copy
from typing import Any, Dict

class DocumentTemplate:
    def __init__(self, content: str, metadata: Dict[str, Any]) -> None:
        self.content = content
        self.metadata = metadata
    
    def clone(self) -> 'DocumentTemplate':
        return DocumentTemplate(
            content=self.content,
            metadata=copy.deepcopy(self.metadata)
        )
    
    def customize(self, new_content: str = None, **kwargs) -> 'DocumentTemplate':
        cloned = self.clone()
        if new_content:
            cloned.content = new_content
        cloned.metadata.update(kwargs)
        return cloned
    
    def __str__(self) -> str:
        return f"Document(content='{self.content[:30]}...', metadata={self.metadata})"

class ReportGenerator:
    def __init__(self) -> None:
        self.templates: Dict[str, DocumentTemplate] = {}
    
    def register_template(self, name: str, template: DocumentTemplate) -> None:
        self.templates[name] = template
    
    def create_from_template(self, template_name: str, **customizations) -> DocumentTemplate:
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        return self.templates[template_name].customize(**customizations)

if __name__ == "__main__":
    generator = ReportGenerator()
    
    monthly_report = DocumentTemplate(
        content="Monthly Performance Report - [DATE]",
        metadata={"type": "report", "frequency": "monthly", "department": "all"}
    )
    
    generator.register_template("monthly", monthly_report)
    
    june_finance = generator.create_from_template(
        "monthly",
        new_content="Monthly Performance Report - June 2024",
        department="finance"
    )
    
    july_sales = generator.create_from_template(
        "monthly",
        new_content="Monthly Performance Report - July 2024",
        department="sales"
    )
    
    print("Original:", monthly_report)
    print("June Finance:", june_finance)
    print("July Sales:", july_sales)