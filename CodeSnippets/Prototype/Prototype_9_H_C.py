import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass
    
    @abstractmethod
    def configure(self, **kwargs):
        pass

class Document(Cloneable):
    def __init__(self, title: str = "Untitled", content: str = "", 
                 metadata: Optional[Dict[str, Any]] = None, attachments: Optional[list] = None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.attachments = attachments or []
        self._version = 1
    
    def clone(self):
        cloned_metadata = copy.deepcopy(self.metadata)
        cloned_attachments = copy.deepcopy(self.attachments)
        new_doc = Document(self.title, self.content, cloned_metadata, cloned_attachments)
        new_doc._version = self._version
        return new_doc
    
    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._version += 1
        return self
    
    def add_attachment(self, attachment):
        self.attachments.append(attachment)
        self._version += 1
    
    def __str__(self):
        return f"Document(title='{self.title}', version={self._version}, attachments={len(self.attachments)})"

class Report(Document):
    def __init__(self, title: str = "Report", content: str = "", 
                 metadata: Optional[Dict[str, Any]] = None, attachments: Optional[list] = None,
                 report_type: str = "general", charts: Optional[list] = None):
        super().__init__(title, content, metadata, attachments)
        self.report_type = report_type
        self.charts = charts or []
    
    def clone(self):
        base_clone = super().clone()
        report_clone = Report(base_clone.title, base_clone.content, 
                            base_clone.metadata, base_clone.attachments,
                            self.report_type, copy.deepcopy(self.charts))
        report_clone._version = base_clone._version
        return report_clone
    
    def add_chart(self, chart):
        self.charts.append(chart)
        self._version += 1
    
    def __str__(self):
        return f"Report(title='{self.title}', type='{self.report_type}', version={self._version}, charts={len(self.charts)})"

class TemplateManager:
    def __init__(self):
        self._templates: Dict[str, Cloneable] = {}
    
    def register_template(self, name: str, template: Cloneable):
        if not isinstance(template, Cloneable):
            raise ValueError("Template must implement Cloneable interface")
        self._templates[name] = template
    
    def create_from_template(self, name: str, **config) -> Optional[Cloneable]:
        template = self._templates.get(name)
        if template is None:
            raise KeyError(f"Template '{name}' not found")
        
        instance = template.clone()
        if config:
            instance.configure(**config)
        return instance
    
    def list_templates(self) -> list:
        return list(self._templates.keys())

if __name__ == "__main__":
    manager = TemplateManager()
    
    base_doc = Document(
        title="Standard Document",
        content="This is a template document.",
        metadata={"author": "System", "category": "template"},
        attachments=["logo.png"]
    )
    
    quarterly_report = Report(
        title="Q1 2024 Report",
        content="Quarterly performance analysis",
        metadata={"department": "Finance", "quarter": "Q1"},
        report_type="financial",
        charts=["revenue_chart", "profit_chart"]
    )
    
    manager.register_template("basic_document", base_doc)
    manager.register_template("quarterly_report", quarterly_report)
    
    print("Available templates:", manager.list_templates())
    
    doc1 = manager.create_from_template("basic_document", 
                                      title="Project Proposal",
                                      content="New project details...")
    
    doc2 = manager.create_from_template("basic_document",
                                      title="Meeting Notes")
    
    report1 = manager.create_from_template("quarterly_report",
                                         title="Q2 2024 Report",
                                         content="Q2 analysis")
    
    doc1.add_attachment("proposal.pdf")
    report1.add_chart("growth_chart")
    
    print(f"Original template: {base_doc}")
    print(f"Document 1: {doc1}")
    print(f"Document 2: {doc2}")
    print(f"Report 1: {report1}")
    print(f"Original quarterly template: {quarterly_report}")