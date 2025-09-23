import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass
    
    @abstractmethod
    def deep_clone(self):
        pass

class SerializableCloneable(Cloneable):
    def __init__(self):
        self._metadata = {}
        self._clone_count = 0
    
    def clone(self):
        cloned = copy.copy(self)
        cloned._clone_count = self._clone_count + 1
        cloned._metadata = self._metadata.copy()
        return cloned
    
    def deep_clone(self):
        cloned = copy.deepcopy(self)
        cloned._clone_count = self._clone_count + 1
        return cloned
    
    def serialize(self) -> str:
        data = {k: v for k, v in self.__dict__.items() 
                if not k.startswith('_') or k in ['_metadata', '_clone_count']}
        return json.dumps(data, default=str)
    
    @classmethod
    def deserialize(cls, data: str):
        obj_data = json.loads(data)
        instance = cls.__new__(cls)
        instance.__dict__.update(obj_data)
        return instance

class Document(SerializableCloneable):
    def __init__(self, title: str = "", content: str = ""):
        super().__init__()
        self.title = title
        self.content = content
        self.sections = []
        self.authors = []
    
    def add_section(self, section_title: str, section_content: str):
        self.sections.append({"title": section_title, "content": section_content})
        return self
    
    def add_author(self, name: str, role: str = "author"):
        self.authors.append({"name": name, "role": role})
        return self
    
    def __str__(self):
        return f"Document(title='{self.title}', sections={len(self.sections)}, authors={len(self.authors)}, generation={self._clone_count})"

class DocumentRegistry:
    def __init__(self):
        self._templates: Dict[str, Document] = {}
    
    def register(self, name: str, template: Document):
        self._templates[name] = template
    
    def create(self, name: str, deep: bool = True) -> Optional[Document]:
        template = self._templates.get(name)
        if template:
            return template.deep_clone() if deep else template.clone()
        return None
    
    def create_from_serialized(self, serialized_data: str) -> Document:
        return Document.deserialize(serialized_data)
    
    def list_templates(self):
        return list(self._templates.keys())

if __name__ == "__main__":
    registry = DocumentRegistry()
    
    report_template = (Document("Annual Report Template", "Executive Summary")
                      .add_section("Financial Overview", "Revenue and expenses")
                      .add_section("Market Analysis", "Industry trends")
                      .add_author("John Doe", "analyst"))
    
    proposal_template = (Document("Project Proposal", "Project description")
                        .add_section("Objectives", "Goals and milestones")
                        .add_author("Jane Smith", "manager"))
    
    registry.register("report", report_template)
    registry.register("proposal", proposal_template)
    
    doc1 = registry.create("report")
    doc1.title = "Q4 2023 Report"
    doc1.add_author("Alice Johnson", "reviewer")
    
    doc2 = registry.create("report", deep=False)
    doc2.title = "Q1 2024 Report"
    
    serialized = doc1.serialize()
    doc3 = registry.create_from_serialized(serialized)
    doc3.title = "Restored Report"
    
    print(f"Original template: {report_template}")
    print(f"Document 1: {doc1}")
    print(f"Document 2: {doc2}")
    print(f"Document 3 (from serialized): {doc3}")
    print(f"Available templates: {registry.list_templates()}")
    print(f"Shared authors reference (shallow): {doc2.authors is report_template.authors}")
    print(f"Independent authors (deep): {doc1.authors is report_template.authors}")