from abc import ABC, abstractmethod
from typing import Type, Dict

class Weapon(ABC):
    @abstractmethod
    def attack(self) -> int:
        pass

class Sword(Weapon):
    def __init__(self, level: int = 1):
        if level < 1:
            raise ValueError("Level must be at least 1")
        self._level = level
        self._damage = 10 * level

    def attack(self) -> int:
        return self._damage

class Bow(Weapon):
    def __init__(self, level: int = 1):
        if level < 1:
            raise ValueError("Level must be at least 1")
        self._level = level
        self._damage = 15 * level

    def attack(self) -> int:
        return self._damage

class WeaponForge:
    def __init__(self):
        self._registry: Dict[str, Type[Weapon]] = {
            "sword": Sword,
            "bow": Bow,
        }

    def register(self, weapon_type: str, weapon_class: Type[Weapon]) -> None:
        self._registry[weapon_type] = weapon_class

    def create(self, weapon_type: str, level: int = 1) -> Weapon:
        if level < 1:
            level = 1
        if weapon_type not in self._registry:
            raise ValueError(f"Unknown weapon type: {weapon_type}")
        return self._registry[weapon_type](level)

if __name__ == "__main__":
    forge = WeaponForge()
    sword = forge.create("sword", 2)
    print(f"Sword attack: {sword.attack()}")
    bow = forge.create("bow", 1)
    print(f"Bow attack: {bow.attack()}")
    try:
        invalid = forge.create("staff", 3)
    except ValueError as e:
        print(f"Error: {e}")
    try:
        low_level = forge.create("sword", 0)
        print(f"Low level sword attack: {low_level.attack()}")
    except ValueError:
        print("Level validation passed via default")
    class Axe(Weapon):
        def __init__(self, level: int = 1):
            if level < 1:
                raise ValueError("Level must be at least 1")
            self._level = level
            self._damage = 12 * level
        def attack(self) -> int:
            return self._damage
    forge.register("axe", Axe)
    axe = forge.create("axe", 3)
    print(f"Axe attack: {axe.attack()}")