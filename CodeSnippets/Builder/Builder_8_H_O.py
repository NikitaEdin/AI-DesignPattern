from dataclasses import dataclass
from typing import Tuple
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Home:
    style: str
    walls: int
    doors: int
    windows: int
    roof: str
    garden: bool
    extras: Tuple[str, ...]


class AssemblerBase(ABC):
    def __init__(self):
        self.reset()

    def reset(self):
        self._style = None
        self._walls = 0
        self._doors = 0
        self._windows = 0
        self._roof = None
        self._garden = False
        self._extras = []
        self._assembled = False
        return self

    def ensure_not_assembled(self):
        if self._assembled:
            raise RuntimeError("Product already assembled. Call reset() before reusing the assembler.")

    def walls(self, count: int):
        self.ensure_not_assembled()
        if count < 1:
            raise ValueError("A home must have at least one wall.")
        self._walls = count
        return self

    def doors(self, count: int):
        self.ensure_not_assembled()
        if count < 0:
            raise ValueError("Door count cannot be negative.")
        self._doors = count
        return self

    def windows(self, count: int):
        self.ensure_not_assembled()
        if count < 0:
            raise ValueError("Window count cannot be negative.")
        self._windows = count
        return self

    def roof(self, kind: str):
        self.ensure_not_assembled()
        if not kind:
            raise ValueError("Roof kind must be specified.")
        self._roof = kind
        return self

    def garden(self, enabled: bool = True):
        self.ensure_not_assembled()
        self._garden = bool(enabled)
        return self

    def add_extra(self, name: str):
        self.ensure_not_assembled()
        if not name:
            raise ValueError("Extra name cannot be empty.")
        self._extras.append(name)
        return self

    @abstractmethod
    def style_name(self) -> str:
        raise NotImplementedError

    def assemble(self) -> Home:
        self.ensure_not_assembled()
        if self._walls < 1:
            raise ValueError("Cannot assemble: no walls configured.")
        if not self._roof:
            raise ValueError("Cannot assemble: roof not configured.")
        self._assembled = True
        product = Home(
            style=self.style_name(),
            walls=self._walls,
            doors=self._doors,
            windows=self._windows,
            roof=self._roof,
            garden=self._garden,
            extras=tuple(self._extras),
        )
        return product


class ModernHomeAssembler(AssemblerBase):
    def style_name(self) -> str:
        return "Modern"

    def assemble(self) -> Home:
        if self._windows < 2:
            raise ValueError("Modern homes require at least 2 windows for natural light.")
        if self._roof not in ("flat", "green", "solar"):
            raise ValueError("Modern homes require a flat, green, or solar roof.")
        return super().assemble()


class RusticHomeAssembler(AssemblerBase):
    def style_name(self) -> str:
        return "Rustic"

    def assemble(self) -> Home:
        if self._doors < 1:
            raise ValueError("Rustic homes require at least one door.")
        if self._roof not in ("thatched", "sloped", "wooden"):
            raise ValueError("Rustic homes require a thatched, sloped, or wooden roof.")
        return super().assemble()


class ConstructionManager:
    def __init__(self, assembler: AssemblerBase):
        self.assembler = assembler

    def create_minimal_residence(self) -> Home:
        return (
            self.assembler
            .reset()
            .walls(4)
            .doors(1)
            .windows(2)
            .roof("flat")
            .assemble()
        )

    def create_family_residence(self) -> Home:
        return (
            self.assembler
            .reset()
            .walls(6)
            .doors(2)
            .windows(6)
            .roof("solar")
            .garden(True)
            .add_extra("garage")
            .assemble()
        )

    def create_custom(self, walls: int, doors: int, windows: int, roof: str, garden: bool, extras=()):
        seq = self.assembler.reset().walls(walls).doors(doors).windows(windows).roof(roof).garden(garden)
        for e in extras:
            seq.add_extra(e)
        return seq.assemble()


if __name__ == "__main__":
    modern = ModernHomeAssembler()
    manager = ConstructionManager(modern)
    home1 = manager.create_minimal_residence()
    print(home1)

    home2 = manager.create_family_residence()
    print(home2)

    rustic = RusticHomeAssembler()
    manager_rustic = ConstructionManager(rustic)
    try:
        incomplete = rustic.reset().doors(0).windows(1).assemble()
    except Exception as e:
        print("Expected error:", e)

    custom = manager_rustic.create_custom(walls=5, doors=1, windows=3, roof="sloped", garden=False, extras=("barn",))
    print(custom)