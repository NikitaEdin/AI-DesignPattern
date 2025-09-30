from __future__ import annotations
from abc import ABC, abstractmethod
import random

class Hero:
    def __init__(self, name: str):
        self.name = name
        self._condition = Vigilant()
        self.hp = 100
        self.mana = 50
    @property
    def condition(self):
        return self._condition
    @condition.setter
    def condition(self, new):
        self._condition = new
    def act(self):
        self._condition.act(self)
    def hit(self, dmg: int):
        self.hp -= dmg
        if self.hp < 30 and not isinstance(self._condition, Critical):
            self.condition = Critical()
    def rest(self):
        self.mana += 10
        if self.mana > 100:
            self.mana = 100
    def __repr__(self):
        return f"{self.name}(hp={self.hp}, mana={self.mana})"

class Condition(ABC):
    @abstractmethod
    def act(self, hero: Hero): ...
    @abstractmethod
    def __repr__(self): ...

class Vigilant(Condition):
    def act(self, hero: Hero):
        hero.mana -= 5
        dmg = random.randint(10, 20)
        print(f"{hero.name} slashes for {dmg} damage")
        if hero.mana < 10:
            hero.condition = Exhausted()
    def __repr__(self):
        return "Vigilant"

class Exhausted(Condition):
    def act(self, hero: Hero):
        hero.hp -= 2
        hero.mana += 3
        print(f"{hero.name} gasps, recovers 3 mana")
        if hero.mana > 30:
            hero.condition = Vigilant()
    def __repr__(self):
        return "Exhausted"

class Critical(Condition):
    def act(self, hero: Hero):
        hero.hp += random.randint(5, 10)
        hero.mana += 5
        print(f"{hero.name} drinks potion")
        if hero.hp >= 50:
            hero.condition = Vigilant()
    def __repr__(self):
        return "Critical"

if __name__ == "__main__":
    h = Hero("Aria")
    for _ in range(15):
        h.act()
        if random.random() < 0.3:
            h.hit(random.randint(5, 15))
        if random.random() < 0.2:
            h.rest()
        print(h, h.condition)