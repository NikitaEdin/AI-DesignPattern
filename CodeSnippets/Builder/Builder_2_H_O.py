from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
import copy

@dataclass(frozen=True)
class Product:
    category: str
    core: str
    engine: Optional[Dict[str, object]]
    features: List[str]
    metadata: Dict[str, object]

    @classmethod
    def from_state(cls, category: str, core: str, engine: Optional[Dict[str, object]],
                   features: List[str], metadata: Dict[str, object]) -> "Product":
        if not core:
            raise ValueError("Product must have a core component")
        features = list(features)
        metadata = dict(metadata)
        if engine is None and "motor" in features:
            raise ValueError("Motor feature requires engine configuration")
        return cls(category=category, core=core, engine=engine, features=features, metadata=metadata)

class AbstractMaker(ABC):
    @abstractmethod
    def reset(self) -> None: ...
    @abstractmethod
    def set_core(self, name: str) -> "AbstractMaker": ...
    @abstractmethod
    def configure_engine(self, specs: Dict[str, object]) -> "AbstractMaker": ...
    @abstractmethod
    def add_feature(self, feature: str) -> "AbstractMaker": ...
    @abstractmethod
    def get_product(self) -> Product: ...

class CarAssembler(AbstractMaker):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._category = "Car"
        self._core: Optional[str] = None
        self._engine: Optional[Dict[str, object]] = None
        self._features: List[str] = []
        self._meta: Dict[str, object] = {}

    def set_core(self, name: str) -> "CarAssembler":
        if not name:
            raise ValueError("Core name cannot be empty")
        self._core = name
        self._meta["core_set"] = True
        return self

    def configure_engine(self, specs: Dict[str, object]) -> "CarAssembler":
        if "power" in specs and specs["power"] <= 0:
            raise ValueError("Engine power must be positive")
        self._engine = dict(specs)
        self._meta["engine_configured"] = True
        return self

    def add_feature(self, feature: str) -> "CarAssembler":
        if feature in self._features:
            return self
        self._features.append(feature)
        return self

    def get_product(self) -> Product:
        product = Product.from_state(self._category, self._core, self._engine, self._features, self._meta)
        self._meta["last_built"] = product
        return product

class BikeAssembler(AbstractMaker):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._category = "Bike"
        self._core: Optional[str] = None
        self._engine: Optional[Dict[str, object]] = None
        self._features: List[str] = []
        self._meta: Dict[str, object] = {}

    def set_core(self, name: str) -> "BikeAssembler":
        if not name:
            raise ValueError("Core name cannot be empty")
        self._core = name
        return self

    def configure_engine(self, specs: Dict[str, object]) -> "BikeAssembler":
        if specs.get("power", 0) > 50:
            raise ValueError("Bike engine power cannot exceed 50")
        self._engine = dict(specs)
        return self

    def add_feature(self, feature: str) -> "BikeAssembler":
        if feature == "sunroof":
            raise ValueError("Sunroof not applicable to bikes")
        self._features.append(feature)
        return self

    def get_product(self) -> Product:
        return Product.from_state(self._category, self._core, self._engine, self._features, self._meta)

class Conductor:
    def assemble_minimal(self, maker: AbstractMaker, core_name: str) -> Product:
        maker.reset()
        maker.set_core(core_name)
        return maker.get_product()

    def assemble_full(self, maker: AbstractMaker, core_name: str,
                      engine_specs: Optional[Dict[str, object]] = None,
                      features: Optional[List[str]] = None) -> Product:
        maker.reset()
        maker.set_core(core_name)
        if engine_specs is not None and hasattr(maker, "configure_engine"):
            maker.configure_engine(engine_specs)
        if features:
            for f in features:
                maker.add_feature(f)
        product = maker.get_product()
        return product

if __name__ == "__main__":
    conductor = Conductor()

    car_maker = CarAssembler()
    car = conductor.assemble_full(
        car_maker,
        core_name="SedanChassis",
        engine_specs={"power": 180, "type": "V6"},
        features=["airbags", "navigation", "motor"]
    )
    print(car)

    bike_maker = BikeAssembler()
    bike_min = conductor.assemble_minimal(bike_maker, core_name="RoadFrame")
    print(bike_min)

    try:
        bike = conductor.assemble_full(
            bike_maker,
            core_name="SportFrame",
            engine_specs={"power": 60},
            features=["lights"]
        )
    except Exception as e:
        print("Error while assembling bike:", e)

    # Reuse car_maker to create a lightweight variant
    light_car = car_maker.reset() or car_maker.set_core("CompactChassis").configure_engine({"power": 120}).add_feature("eco_mode").get_product()
    print(light_car)