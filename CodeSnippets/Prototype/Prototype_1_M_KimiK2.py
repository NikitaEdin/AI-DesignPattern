import copy
from abc import ABC, abstractmethod
from typing import Dict

class BaseComponent(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def duplicate(self):
        pass

class Document(BaseComponent):
    def __init__(self, name: str, content: str, metadata: Dict[str, str]):
        super().__init__(name)
        self.content = content
        self.metadata = metadata.copy()
    
    def duplicate(self):
        new_metadata = copy.deepcopy(self.metadata)
        return Document(f"{self.name}_copy", self.content, new_metadata)
    
    def update_metadata(self, key: str, value:str):
        self.metadata[key] = value

class Spreadsheet(BaseComponent):
    def __init__(self, name: str, data: list):
        super().__init__(name)
        self.data = data
    
    def duplicate(self):
        new_data = copy.deepcopy(self.data)
        return Spreadsheet(f"{self.name}_copy", new_data)
    
    def add_row(self, row):
        self.data.append(row)

class ComponentRegistry:
    _components: Dict[str, BaseComponent] = {}
    
    @classmethod
    def register(cls, component: BaseComponent):
        cls._components[component.name] = component
    
    @classmethod
    def duplicate_by_name(cls, name: str):
        if name not in cls._components:
            raise ValueError("Component not found")
        return cls._components[name].duplicate()

if __name__ == "__main__":
    doc = Document("Report", "Annual Report", {"author": "John", "year": "2023"})
    sheet = Spreadsheet("Sales", [["Q1", 1000], ["Q2", 1500]])
    
    ComponentRegistry.register(doc)
    ComponentRegistry.register(sheet)

    doc_copy = ComponentRegistry.duplicate_by_name("Report")
    sheet_copy = ComponentRegistry.duplicate_by_name("Sales")

    doc_copy.update_metadata("status", "draft")
    sheet_copy.add_row(["Q3", 2000])