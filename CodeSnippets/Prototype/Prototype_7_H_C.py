import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json


class Cloneable(ABC):
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    @abstractmethod
    def deep_clone(self) -> 'Cloneable':
        pass


class GameCharacter(Cloneable):
    def __init__(self, name: str, health: int, equipment: Optional[Dict[str, Any]] = None):
        self._name = name
        self._health = health
        self._equipment = equipment or {}
        self._skills = []
        self._metadata = {"created_count": 0, "clone_generation": 0}
    
    def add_skill(self, skill: str) -> None:
        self._skills.append(skill)
    
    def equip_item(self, slot: str, item: Dict[str, Any]) -> None:
        self._equipment[slot] = item
    
    def clone(self) -> 'GameCharacter':
        cloned = GameCharacter(self._name, self._health)
        cloned._equipment = self._equipment.copy()
        cloned._skills = self._skills.copy()
        cloned._metadata = self._metadata.copy()
        cloned._metadata["clone_generation"] += 1
        return cloned
    
    def deep_clone(self) -> 'GameCharacter':
        cloned = GameCharacter(self._name, self._health)
        cloned._equipment = copy.deepcopy(self._equipment)
        cloned._skills = copy.deepcopy(self._skills)
        cloned._metadata = copy.deepcopy(self._metadata)
        cloned._metadata["clone_generation"] += 1
        return cloned
    
    def __str__(self) -> str:
        return f"{self._name}(HP:{self._health}, Gen:{self._metadata['clone_generation']})"


class Vehicle(Cloneable):
    def __init__(self, model: str, specs: Dict[str, Any]):
        self.model = model
        self.specs = specs
        self.components = {}
    
    def add_component(self, name: str, component: Dict[str, Any]) -> None:
        self.components[name] = component
    
    def clone(self) -> 'Vehicle':
        cloned = Vehicle(self.model, self.specs.copy())
        cloned.components = self.components.copy()
        return cloned
    
    def deep_clone(self) -> 'Vehicle':
        cloned = Vehicle(self.model, copy.deepcopy(self.specs))
        cloned.components = copy.deepcopy(self.components)
        return cloned


class Registry:
    def __init__(self):
        self._templates: Dict[str, Cloneable] = {}
    
    def register(self, key: str, template: Cloneable) -> None:
        self._templates[key] = template
    
    def create(self, key: str, deep: bool = False) -> Optional[Cloneable]:
        template = self._templates.get(key)
        if template:
            return template.deep_clone() if deep else template.clone()
        return None
    
    def create_batch(self, key: str, count: int, deep: bool = False) -> list:
        return [self.create(key, deep) for _ in range(count)]


def main():
    registry = Registry()
    
    warrior = GameCharacter("Warrior", 100)
    warrior.add_skill("Sword Mastery")
    warrior.equip_item("weapon", {"name": "Steel Sword", "damage": 25, "enchants": ["sharpness"]})
    warrior.equip_item("armor", {"name": "Chain Mail", "defense": 15})
    
    car_template = Vehicle("SportsCar", {"engine": "V8", "horsepower": 450})
    car_template.add_component("turbo", {"type": "twin", "boost": 1.5})
    
    registry.register("basic_warrior", warrior)
    registry.register("sports_car", car_template)
    
    squad = registry.create_batch("basic_warrior", 3)
    for i, member in enumerate(squad):
        print(f"Squad Member {i+1}: {member}")
    
    squad[0].equip_item("weapon", {"name": "Magic Sword", "damage": 50})
    
    print("\nAfter modification:")
    for i, member in enumerate(squad):
        weapon = member._equipment.get("weapon", {}).get("name", "None")
        print(f"Squad Member {i+1}: {member}, Weapon: {weapon}")
    
    deep_car = registry.create("sports_car", deep=True)
    shallow_car = registry.create("sports_car", deep=False)
    
    deep_car.add_component("nitrous", {"capacity": "10L"})
    shallow_car.specs["horsepower"] = 500
    
    print(f"\nOriginal car HP: {car_template.specs['horsepower']}")
    print(f"Deep clone components: {len(deep_car.components)}")
    print(f"Shallow clone components: {len(shallow_car.components)}")


if __name__ == "__main__":
    main()