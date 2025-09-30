import json
from typing import Optional, List, Dict, Any

class EngineSpec:
    def __init__(self, power_kw: int, torque_nm: int, fuel: str):
        self.power_kw = power_kw
        self.torque_nm = torque_nm
        self.fuel = fuel

class Vehicle:
    def __init__(self):
        self.make: Optional[str] = None
        self.model: Optional[str] = None
        self.engine: Optional[EngineSpec] = None
        self.color: str = "white"
        self.features: List[str] = []
        self.config: Dict[str, Any] = {}

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=2, default=lambda o: o.__dict__)

class VehicleAssembler:
    def __init__(self):
        self._product = Vehicle()

    def set_make(self, make: str) -> 'VehicleAssembler':
        if not make or not make.strip():
            raise ValueError("Make must be non-empty")
        self._product.make = make.strip()
        return self

    def set_model(self, model: str) -> 'VehicleAssembler':
        if not model or not model.strip():
            raise ValueError("Model must be non-empty")
        self._product.model = model.strip()
        return self

    def set_engine(self, power_kw: int, torque_nm: int, fuel: str) -> 'VehicleAssembler':
        if power_kw <= 0 or torque_nm <= 0:
            raise ValueError("Engine specs must be positive")
        self._product.engine = EngineSpec(power_kw, torque_nm, fuel)
        return self

    def set_color(self, color: str) -> 'VehicleAssembler':
        if not color or not color.strip():
            raise ValueError("Color must be non-empty")
        self._product.color = color.strip()
        return self

    def add_feature(self, feature: str) -> 'VehicleAssembler':
        if not feature or not feature.strip():
            raise ValueError("Feature must be non-empty")
        self._product.features.append(feature.strip())
        return self

    def configure(self, **kwargs: Any) -> 'VehicleAssembler':
        self._product.config.update(kwargs)
        return self

    def assemble(self) -> Vehicle:
        if not self._product.make or not self._product.model or not self._product.engine:
            raise RuntimeError("Make, model and engine are required")
        finalized = self._product
        self._product = Vehicle()
        return finalized

if __name__ == "__main__":
    assembler = VehicleAssembler()
    car = (assembler
           .set_make("Tesla")
           .set_model("Model S")
           .set_engine(480, 1000, "Electric")
           .set_color("Midnight Silver")
           .add_feature("Autopilot")
           .add_feature("Panoramic Roof")
           .configure(wheels=21, interior="white leather")
           .assemble())
    print(car)