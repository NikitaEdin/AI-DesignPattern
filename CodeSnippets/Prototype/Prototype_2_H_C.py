import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Cloneable(ABC):
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

class ConfigurableShape(Cloneable):
    def __init__(self, shape_type: str, properties: Dict[str, Any]):
        self._shape_type = shape_type
        self._properties = properties.copy()
        self._metadata = {'created_from': 'original', 'clone_depth': 0}
    
    def clone(self) -> 'ConfigurableShape':
        cloned_properties = copy.deepcopy(self._properties)
        cloned = ConfigurableShape(self._shape_type, cloned_properties)
        cloned._metadata = {
            'created_from': 'clone',
            'clone_depth': self._metadata['clone_depth'] + 1
        }
        return cloned
    
    def update_property(self, key: str, value: Any) -> None:
        self._properties[key] = value
    
    def get_property(self, key: str) -> Any:
        return self._properties.get(key)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ConfigurableShape):
            return False
        return (self._shape_type == other._shape_type and 
                self._properties == other._properties)
    
    def __str__(self) -> str:
        return f"{self._shape_type}: {self._properties} (depth: {self._metadata['clone_depth']})"

class ShapeRegistry:
    def __init__(self):
        self._templates: Dict[str, ConfigurableShape] = {}
    
    def register(self, name: str, template: ConfigurableShape) -> None:
        if not isinstance(template, ConfigurableShape):
            raise TypeError("Template must be a ConfigurableShape instance")
        self._templates[name] = template
    
    def create(self, name: str) -> Optional[ConfigurableShape]:
        template = self._templates.get(name)
        return template.clone() if template else None
    
    def create_customized(self, name: str, modifications: Dict[str, Any]) -> Optional[ConfigurableShape]:
        instance = self.create(name)
        if instance:
            for key, value in modifications.items():
                instance.update_property(key, value)
        return instance
    
    def list_templates(self) -> list:
        return list(self._templates.keys())

class Document(Cloneable):
    def __init__(self, title: str, content: str = ""):
        self.title = title
        self.content = content
        self.sections = []
        self.formatting = {'font': 'Arial', 'size': 12}
    
    def clone(self) -> 'Document':
        cloned = Document(self.title, self.content)
        cloned.sections = copy.deepcopy(self.sections)
        cloned.formatting = self.formatting.copy()
        return cloned
    
    def add_section(self, section: str) -> None:
        self.sections.append(section)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Document):
            return False
        return (self.title == other.title and 
                self.content == other.content and
                self.sections == other.sections)
    
    def __str__(self) -> str:
        return f"Document: {self.title} ({len(self.sections)} sections)"

if __name__ == "__main__":
    registry = ShapeRegistry()
    
    circle_template = ConfigurableShape("Circle", {
        "radius": 10, "color": "blue", "position": {"x": 0, "y": 0}
    })
    
    rectangle_template = ConfigurableShape("Rectangle", {
        "width": 20, "height": 15, "color": "red", "position": {"x": 0, "y": 0}
    })
    
    registry.register("default_circle", circle_template)
    registry.register("default_rectangle", rectangle_template)
    
    circle1 = registry.create("default_circle")
    circle2 = registry.create_customized("default_circle", {
        "radius": 25, "color": "green", "position": {"x": 100, "y": 50}
    })
    
    print(f"Original template: {circle_template}")
    print(f"Circle 1: {circle1}")
    print(f"Circle 2: {circle2}")
    
    doc_template = Document("Report Template", "This is a standard report.")
    doc_template.add_section("Introduction")
    doc_template.add_section("Analysis")
    
    doc1 = doc_template.clone()
    doc1.title = "Q1 Report"
    doc1.add_section("Conclusions")
    
    print(f"\nTemplate: {doc_template}")
    print(f"Cloned document: {doc1}")
    print(f"Templates equal: {doc_template == doc1}")