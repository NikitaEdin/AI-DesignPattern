import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import weakref

class Cloneable(ABC):
    def __init__(self):
        self._registry = weakref.WeakValueDictionary()
    
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    def register_instance(self, name: str):
        CloneRegistry.register(name, self)
        return self
    
    def _deep_clone(self) -> 'Cloneable':
        return copy.deepcopy(self)
    
    def _shallow_clone(self) -> 'Cloneable':
        return copy.copy(self)

class CloneRegistry:
    _instances: Dict[str, Cloneable] = {}
    
    @classmethod
    def register(cls, name: str, instance: Cloneable):
        cls._instances[name] = instance
    
    @classmethod
    def get_clone(cls, name: str) -> Optional[Cloneable]:
        instance = cls._instances.get(name)
        return instance.clone() if instance else None
    
    @classmethod
    def list_registered(cls) -> list:
        return list(cls._instances.keys())

class Document(Cloneable):
    def __init__(self, title: str = "", content: str = "", metadata: Dict[str, Any] = None):
        super().__init__()
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self._version = 1
    
    def clone(self) -> 'Document':
        cloned = self._deep_clone()
        cloned._version = self._version + 1
        return cloned
    
    def update_content(self, content: str):
        self.content = content
        self._version += 1
    
    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value
    
    def __str__(self):
        return f"Document(title='{self.title}', version={self._version})"

class GraphicsShape(Cloneable):
    def __init__(self, x: int = 0, y: int = 0, color: str = "black"):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.transformations = []
    
    def clone(self) -> 'GraphicsShape':
        return self._deep_clone()
    
    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        self.transformations.append(f"move({dx}, {dy})")
    
    def set_color(self, color: str):
        self.color = color
    
    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, color='{self.color}')"

class Rectangle(GraphicsShape):
    def __init__(self, x: int = 0, y: int = 0, width: int = 10, height: int = 10, color: str = "black"):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
    
    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.transformations.append(f"resize({width}, {height})")

class Circle(GraphicsShape):
    def __init__(self, x: int = 0, y: int = 0, radius: int = 5, color: str = "black"):
        super().__init__(x, y, color)
        self.radius = radius
    
    def set_radius(self, radius: int):
        self.radius = radius
        self.transformations.append(f"set_radius({radius})")

if __name__ == "__main__":
    template_doc = Document("Template", "Default content", {"author": "System"}).register_instance("default_doc")
    
    red_circle = Circle(10, 10, 15, "red").register_instance("red_circle")
    blue_rect = Rectangle(0, 0, 20, 30, "blue").register_instance("blue_rect")
    
    doc1 = CloneRegistry.get_clone("default_doc")
    doc1.title = "Report 1"
    doc1.update_content("Custom report content")
    
    doc2 = CloneRegistry.get_clone("default_doc")
    doc2.title = "Report 2"
    doc2.add_metadata("department", "Engineering")
    
    circle1 = CloneRegistry.get_clone("red_circle")
    circle1.move(5, 5)
    circle1.set_radius(20)
    
    rect1 = CloneRegistry.get_clone("blue_rect")
    rect1.set_color("green")
    rect1.resize(40, 60)
    
    print("Cloned documents:")
    print(doc1, "- Content length:", len(doc1.content))
    print(doc2, "- Metadata:", doc2.metadata)
    
    print("\nCloned shapes:")
    print(circle1, "- Transformations:", len(circle1.transformations))
    print(rect1, "- Transformations:", len(rect1.transformations))
    
    print("\nRegistered templates:", CloneRegistry.list_registered())