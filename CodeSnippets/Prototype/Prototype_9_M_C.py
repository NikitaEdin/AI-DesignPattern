import copy
from abc import ABC, abstractmethod

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass

class Character(Cloneable):
    def __init__(self, name, health, weapon, armor):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.level = 1
        self.experience = 0

    def clone(self):
        return copy.deepcopy(self)
    
    def customize(self, name=None, weapon=None, armor=None):
        if name:
            self.name = name
        if weapon:
            self.weapon = weapon
        if armor:
            self.armor = armor
        return self

    def __str__(self):
        return f"{self.name} (Lv.{self.level}) - HP:{self.health} | {self.weapon} | {self.armor}"

class GameRegistry:
    def __init__(self):
        self._templates = {}
    
    def register_template(self, key, template):
        if not isinstance(template, Cloneable):
            raise ValueError("Template must implement Cloneable interface")
        self._templates[key] = template
    
    def create_character(self, template_key):
        if template_key not in self._templates:
            raise KeyError(f"Template '{template_key}' not found")
        return self._templates[template_key].clone()

if __name__ == "__main__":
    registry = GameRegistry()
    
    warrior_template = Character("Warrior", 100, "Steel Sword", "Chainmail")
    mage_template = Character("Mage", 70, "Magic Staff", "Robes")
    
    registry.register_template("warrior", warrior_template)
    registry.register_template("mage", mage_template)
    
    player1 = registry.create_character("warrior").customize("Aragorn", weapon="Legendary Blade")
    player2 = registry.create_character("mage").customize("Gandalf", armor="Mystic Cloak")
    player3 = registry.create_character("warrior").customize("Boromir")
    
    print(player1)
    print(player2)
    print(player3)