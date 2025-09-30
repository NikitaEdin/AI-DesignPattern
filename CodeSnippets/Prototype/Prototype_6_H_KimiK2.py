import copy
from typing import Any, Dict, Optional

class ShapeBlueprint:
    def __init__(self, dimensions: Dict[str, Any], color: str = "white", material: str = "plastic"):
        self.dimensions = dimensions
        self.color = color
        self.material = material
        self._cache: Optional[Any] = None
    
    def replicate(self) -> 'ShapeBlueprint':
        try:
            duplicate = copy.deepcopy(self)
            duplicate._cache = None
            return duplicate
        except Exception as e:
            raise RuntimeError(f"Replication failed: {e}") from e
    
    def modify(self, **changes) -> 'ShapeBlueprint':
        duplicate = self.replicate()
        for key, value in changes.items():
            if hasattr(duplicate, key):
                setattr(duplicate, key, value)
            elif key in duplicate.dimensions:
                duplicate.dimensions[key] = value
            else:
                raise AttributeError(f"Invalid modification: {key}")
        return duplicate
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.dimensions}, {self.color}, {self.material})"

class Registry:
    def __init__(self):
        self._templates: Dict[str, ShapeBlueprint] = {}
    
    def register(self, name: str, template: ShapeBlueprint) -> None:
        self._templates[name] = template
    
    def get(self, name: str) -> ShapeBlueprint:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found")
        return self._templates[name].replicate()
    
    def list(self) -> list[str]:
        return list(self._templates.keys())

if __name__ == "__main__":
    registry = Registry()
    
    circle = ShapeBlueprint({"radius": 5}, color="red", material="wood")
    cube = ShapeBlueprint({"side": 10}, color="blue")
    
    registry.register("basic_circle", circle)
    registry.register("basic_cube", cube)
    
    circle1 = registry.get("basic_circle")
    circle2 = registry.get("basic_circle")
    
    circle2.color = "green"
    circle2.dimensions["radius"] = 8
    
    modified_cube = cube.modify(color="black", material="metal", side=15)
    
    print("Original circle:", circle)
    print("Circle1:", circle1)
    print("Circle2:", circle2)
    print("Modified cube:", modified_cube)
    print("Registry templates:", registry.list())