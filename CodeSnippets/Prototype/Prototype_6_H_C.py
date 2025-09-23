import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Cloneable(ABC):
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        pass

class GameCharacter(Cloneable):
    def __init__(self, name: str, level: int, equipment: Optional[Dict] = None, 
                 stats: Optional[Dict] = None):
        self.name = name
        self.level = level
        self.equipment = equipment or {}
        self.stats = stats or {"health": 100, "mana": 50, "strength": 10}
        self._creation_history = []
    
    def clone(self) -> 'GameCharacter':
        cloned = GameCharacter(
            name=f"{self.name}_copy",
            level=self.level,
            equipment=copy.deepcopy(self.equipment),
            stats=copy.deepcopy(self.stats)
        )
        cloned._creation_history = self._creation_history.copy()
        cloned._creation_history.append(f"Cloned from {self.name}")
        return cloned
    
    def get_type(self) -> str:
        return "character"
    
    def upgrade_equipment(self, item: str, value: Any):
        self.equipment[item] = value
    
    def modify_stats(self, stat: str, value: int):
        if stat in self.stats:
            self.stats[stat] = value

class Weapon(Cloneable):
    def __init__(self, name: str, damage: int, enchantments: Optional[Dict] = None):
        self.name = name
        self.damage = damage
        self.enchantments = enchantments or {}
        self.durability = 100
    
    def clone(self) -> 'Weapon':
        cloned = Weapon(
            name=f"{self.name}_replica",
            damage=self.damage,
            enchantments=copy.deepcopy(self.enchantments)
        )
        cloned.durability = self.durability
        return cloned
    
    def get_type(self) -> str:
        return "weapon"
    
    def add_enchantment(self, name: str, power: int):
        self.enchantments[name] = power

class ObjectRegistry:
    def __init__(self):
        self._objects: Dict[str, Cloneable] = {}
        self._version_history: Dict[str, int] = {}
    
    def register(self, key: str, obj: Cloneable):
        self._objects[key] = obj
        self._version_history[key] = 1
    
    def create(self, key: str) -> Optional[Cloneable]:
        if key in self._objects:
            cloned = self._objects[key].clone()
            self._version_history[key] += 1
            return cloned
        return None
    
    def update_template(self, key: str, obj: Cloneable):
        if key in self._objects:
            self._objects[key] = obj
    
    def get_creation_count(self, key: str) -> int:
        return self._version_history.get(key, 0) - 1
    
    def list_templates(self) -> Dict[str, str]:
        return {key: obj.get_type() for key, obj in self._objects.items()}

if __name__ == "__main__":
    registry = ObjectRegistry()
    
    warrior_template = GameCharacter(
        "Warrior", 
        level=10,
        equipment={"armor": "chainmail", "shield": "iron_shield"},
        stats={"health": 150, "mana": 30, "strength": 20}
    )
    
    fire_sword = Weapon("Flameblade", damage=50)
    fire_sword.add_enchantment("fire_damage", 15)
    fire_sword.add_enchantment("burning", 5)
    
    registry.register("base_warrior", warrior_template)
    registry.register("fire_weapon", fire_sword)
    
    print("Creating warriors and weapons...")
    warrior1 = registry.create("base_warrior")
    warrior2 = registry.create("base_warrior")
    
    sword1 = registry.create("fire_weapon")
    sword2 = registry.create("fire_weapon")
    
    warrior1.name = "Aragorn"
    warrior1.upgrade_equipment("weapon", "legendary_sword")
    warrior1.modify_stats("strength", 25)
    
    sword2.add_enchantment("ice_damage", 10)
    sword2.durability = 80
    
    print(f"Warrior 1: {warrior1.name}, Level: {warrior1.level}, Strength: {warrior1.stats['strength']}")
    print(f"Warrior 2: {warrior2.name}, Level: {warrior2.level}, Strength: {warrior2.stats['strength']}")
    print(f"Original template strength: {warrior_template.stats['strength']}")
    
    print(f"Sword 1 enchantments: {sword1.enchantments}")
    print(f"Sword 2 enchantments: {sword2.enchantments}")
    print(f"Original sword enchantments: {fire_sword.enchantments}")
    
    print(f"Templates available: {registry.list_templates()}")
    print(f"Warriors created: {registry.get_creation_count('base_warrior')}")
    print(f"Weapons created: {registry.get_creation_count('fire_weapon')}")