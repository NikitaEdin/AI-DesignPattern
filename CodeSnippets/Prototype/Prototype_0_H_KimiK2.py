import copy
from typing import Dict, Any, Optional

class ShapeCache:
    _registry: Dict[str, 'Shape'] = {}
    
    @classmethod
    def register(cls, key: str, shape: 'Shape') -> None:
        cls._registry[key] = shape
    
    @classmethod
    def get(cls, key: str) -> Optional['Shape']:
        if key in cls._registry:
            return cls._registry[key].replicate()
        return None

class Shape:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height
        self.metadata: Dict[str, Any] = {}
    
    def replicate(self) -> 'Shape':
        new_obj = copy.deepcopy(self)
        new_obj.post_clone()
        return new_obj
    
    def post_clone(self) -> None:
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.width}x{self.height})"

class Rectangle(Shape):
    def __init__(self, width: int = 10, height: int = 20, corner_radius: int = 0):
        super().__init__(width, height)
        self.corner_radius = corner_radius
        self.metadata['type'] = 'rectangle'
    
    def post_clone(self) -> None:
        self.metadata['cloned'] = True

class Circle(Shape):
    def __init__(self, radius: int = 5):
        super().__init__(radius * 2, radius * 2)
        self.radius = radius
        self.metadata['type'] = 'circle'
    
    def post_clone(self) -> None:
        self.metadata['cloned'] = True

if __name__ == "__main__":
    rect = Rectangle(15, 30, 3)
    circle = Circle(10)
    
    ShapeCache.register('rect', rect)
    ShapeCache.register('circle', circle)
    
    cloned_rect = ShapeCache.get('rect')
    cloned_circle = ShapeCache.get('circle')
    
    print("Original:", rect)
    print("Cloned:", cloned_rect)
    print("Metadata:", cloned_rect.metadata)
    
    print("Original:", circle)
    print("Cloned:", cloned_circle)
    print("Metadata:", cloned_circle.metadata)