from abc import ABC, abstractmethod
from typing import Optional, List

class Engine:
    def __init__(self, horsepower: int) -> None:
        self.horsepower = horsepower

class Chassis:
    def __init__(self, material: str) -> None:
        self.material = material

class Automobile:
    def __init__(self) -> None:
        self.engine: Optional[Engine] = None
        self.chassis: Optional[Chassis] = None
        self.wheels: int = 0
        self.extras: List[str] = []

    def __str__(self) -> str:
        extras = ", ".join(self.extras) if self.extras else "none"
        return (f"Auto: {self.wheels} wheels, "
                f"{self.engine.horsepower}hp, "
                f"{self.chassis.material} chassis, extras: {extras}")

class AssemblyProtocol(ABC):
    @abstractmethod
    def mount_engine(self, horsepower: int) -> "AssemblyProtocol": ...
    @abstractmethod
    def mount_chassis(self, material: str) -> "AssemblyProtocol": ...
    @abstractmethod
    def attach_wheels(self, count: int) -> "AssemblyProtocol": ...
    @abstractmethod
    def add_extra(self, item: str) -> "AssemblyProtocol": ...
    @abstractmethod
    def retrieve_product(self) -> Automobile: ...

class SportsAssembler(AssemblyProtocol):
    def __init__(self) -> None:
        self.auto = Automobile()
    def mount_engine(self, horsepower: int) -> "SportsAssembler":
        self.auto.engine = Engine(horsepower)
        return self
    def mount_chassis(self, material: str) -> "SportsAssembler":
        self.auto.chassis = Chassis(material)
        return self
    def attach_wheels(self, count: int) -> "SportsAssembler":
        self.auto.wheels = count
        return self
    def add_extra(self, item: str) -> "SportsAssembler":
        self.auto.extras.append(item)
        return self
    def retrieve_product(self) -> Automobile:
        return self.auto

class OffRoadAssembler(AssemblyProtocol):
    def __init__(self) -> None:
        self.auto = Automobile()
    def mount_engine(self, horsepower: int) -> "OffRoadAssembler":
        self.auto.engine = Engine(horsepower)
        return self
    def mount_chassis(self, material: str) -> "OffRoadAssembler":
        self.auto.chassis = Chassis(material)
        return self
    def attach_wheels(self, count: int) -> "OffRoadAssembler":
        self.auto.wheels = count
        return self
    def add_extra(self, item: str) -> "OffRoadAssembler":
        self.auto.extras.append(item)
        return self
    def retrieve_product(self) -> Automobile:
        return self.auto

class WorkshopDirector:
    def construct(self, assembler: AssemblyProtocol) -> Automobile:
        return (assembler
                .mount_engine(450)
                .mount_chassis("carbon fiber")
                .attach_wheels(4)
                .add_extra("turbo")
                .add_extra("racing stripes")
                .retrieve_product())

if __name__ == "__main__":
    director = WorkshopDirector()
    sports_car = director.construct(SportsAssembler())
    print(sports_car)
    offroader = (OffRoadAssembler()
                 .mount_engine(300)
                 .mount_chassis("steel")
                 .attach_wheels(4)
                 .add_extra("winch")
                 .add_extra("roof rack")
                 .retrieve_product())
    print(offroader)