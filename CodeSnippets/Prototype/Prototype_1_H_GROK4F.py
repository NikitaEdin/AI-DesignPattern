import copy
from abc import ABC, abstractmethod
from typing import Dict, Any

class VehicleComponent(ABC):
    @abstractmethod
    def clone(self) -> 'VehicleComponent':
        pass

class Engine(VehicleComponent):
    def __init__(self, horsepower: int, fuel_type: str):
        self.horsepower = horsepower
        self.fuel_type = fuel_type

    def clone(self) -> 'Engine':
        return Engine(self.horsepower, self.fuel_type)

    def __repr__(self):
        return f"Engine({self.horsepower}hp, {self.fuel_type})"

class Car(VehicleComponent):
    def __init__(self, model: str, engine: Engine = None):
        self.model = model
        self.engine = engine or Engine(150, "gasoline")
        self.color = "white"
        self.components = []  # List for nested components

    def clone(self) -> 'Car':
        cloned = Car(self.model)
        cloned.engine = copy.deepcopy(self.engine)  # Deep copy for nested
        cloned.color = self.color
        cloned.components = [comp.clone() for comp in self.components]  # Deep clone list
        return cloned

    def add_component(self, component: VehicleComponent):
        self.components.append(component)

    def change_color(self, color: str):
        self.color = color

    def upgrade_engine(self, horsepower: int):
        self.engine.horsepower = horsepower

    def __repr__(self):
        return f"Car(model='{self.model}', color='{self.color}', engine={self.engine})"

class VehicleRegistry:
    def __init__(self):
        self._prototypes: Dict[str, VehicleComponent] = {}

    def register(self, key: str, prototype: VehicleComponent):
        if not isinstance(prototype, VehicleComponent):
            raise ValueError("Only VehicleComponent instances can be registered")
        self._prototypes[key] = prototype

    def create_clone(self, key: str, **kwargs) -> VehicleComponent:
        if key not in self._prototypes:
            raise KeyError(f"No prototype registered with key '{key}'")
        cloned = copy.deepcopy(self._prototypes[key])  # Deep copy from registry
        if hasattr(cloned, 'color') and kwargs.get('color'):
            cloned.change_color(kwargs['color'])
        if hasattr(cloned, 'upgrade_engine') and kwargs.get('horsepower'):
            cloned.upgrade_engine(kwargs['horsepower'])
        return cloned

    def get_keys(self) -> list:
        return list(self._prototypes.keys())

def main():
    registry = VehicleRegistry()

    # Create initial prototypes
    sedan = Car("Sedan")
    sedan.add_component(Engine(100, "electric"))  # Nested component
    registry.register("sedan", sedan)

    suv = Car("SUV", Engine(300, "diesel"))
    registry.register("suv", suv)

    print("Available models:", registry.get_keys())

    # Clone with modifications
    cloned_sedan = registry.create_clone("sedan", color="red", horsepower=200)
    cloned_suv = registry.create_clone("suv")

    print("\nOriginal Sedan:", sedan)
    print("Cloned Sedan (modified):", cloned_sedan)

    # Verify independence
    cloned_sedan.change_color("blue")
    print("\nAfter modifying clone - Original Sedan:", sedan)
    print("Cloned Sedan:", cloned_sedan)

    # Edge case: Attempt invalid clone
    try:
        invalid = registry.create_clone("invalid_key")
    except KeyError as e:
        print(f"\nEdge case handled: {e}")

    # Demonstrate deep copy for nested
    print("\nOriginal SUV engine:", suv.engine)
    cloned_suv.upgrade_engine(350)
    print("Cloned SUV engine (after upgrade):", cloned_suv.engine)
    print("Original SUV engine (unchanged):", suv.engine)

if __name__ == "__main__":
    main()