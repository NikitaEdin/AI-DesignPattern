from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Vehicle:
    frame: Optional[str] = None
    engine: Optional[str] = None
    wheels: Optional[int] = None
    interior: Optional[str] = None
    extras: List[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        return all([self.frame, self.engine, self.wheels and self.wheels > 0, self.interior])


class AssemblerInterface(ABC):
    @abstractmethod
    def start_new(self) -> None:
        pass

    @abstractmethod
    def set_frame(self) -> None:
        pass

    @abstractmethod
    def set_engine(self) -> None:
        pass

    @abstractmethod
    def add_wheels(self) -> None:
        pass

    @abstractmethod
    def set_interior(self) -> None:
        pass

    @abstractmethod
    def apply_options(self, options: Dict[str, bool]) -> None:
        pass

    @abstractmethod
    def get_vehicle(self) -> Vehicle:
        pass


class SportsCarAssembler(AssemblerInterface):
    def __init__(self):
        self.start_new()

    def start_new(self) -> None:
        self._product = Vehicle()

    def set_frame(self) -> None:
        self._product.frame = "Lightweight carbon fiber frame"

    def set_engine(self) -> None:
        self._product.engine = "V8 High-performance"

    def add_wheels(self) -> None:
        self._product.wheels = 4

    def set_interior(self) -> None:
        self._product.interior = "Sport bucket seats"

    def apply_options(self, options: Dict[str, bool]) -> None:
        if options.get("sunroof"):
            self._product.extras.append("Panoramic sunroof")
        if options.get("track_package"):
            self._product.extras.append("Track-tuned suspension")

    def get_vehicle(self) -> Vehicle:
        if not self._product.is_complete():
            raise RuntimeError("Incomplete vehicle: missing required components.")
        finished = self._product
        self.start_new()
        return finished


class SuvAssembler(AssemblerInterface):
    def __init__(self):
        self.start_new()

    def start_new(self) -> None:
        self._product = Vehicle()

    def set_frame(self) -> None:
        self._product.frame = "Reinforced steel frame"

    def set_engine(self) -> None:
        self._product.engine = "V6 Efficient"

    def add_wheels(self) -> None:
        self._product.wheels = 4

    def set_interior(self) -> None:
        self._product.interior = "Comfort seating"

    def apply_options(self, options: Dict[str, bool]) -> None:
        if options.get("tow_package"):
            self._product.extras.append("Heavy-duty tow hitch")
        if options.get("roof_rack"):
            self._product.extras.append("Roof rack")

    def get_vehicle(self) -> Vehicle:
        if not self._product.is_complete():
            raise RuntimeError("Incomplete vehicle: missing required components.")
        finished = self._product
        self.start_new()
        return finished


class AssemblyManager:
    def assemble_complete(self, assembler: AssemblerInterface, options: Optional[Dict[str, bool]] = None) -> Vehicle:
        options = options or {}
        assembler.start_new()
        assembler.set_frame()
        assembler.set_engine()
        assembler.add_wheels()
        assembler.set_interior()
        assembler.apply_options(options)
        return assembler.get_vehicle()

    def assemble_partial_for_inspection(self, assembler: AssemblerInterface) -> Vehicle:
        assembler.start_new()
        assembler.set_frame()
        assembler.set_engine()
        assembler.add_wheels()
        if not assembler._product.is_complete():
            assembler._product.interior = "Temporary inspection seats"
        return assembler.get_vehicle()


if __name__ == "__main__":
    manager = AssemblyManager()
    sports = SportsCarAssembler()
    suv = SuvAssembler()

    car1 = manager.assemble_complete(sports, {"sunroof": True, "track_package": False})
    car2 = manager.assemble_complete(suv, {"tow_package": True})

    print(car1)
    print(car2)

    try:
        incomplete = SuvAssembler()
        incomplete.set_frame()
        incomplete.set_engine()
        print(incomplete.get_vehicle())
    except RuntimeError as e:
        print("Error:", e)