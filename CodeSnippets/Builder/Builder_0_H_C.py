from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Product:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._metadata: Dict[str, str] = {}
    
    def add_component(self, name: str, component: Any) -> None:
        if not name or component is None:
            raise ValueError("Component name and value cannot be empty")
        self._components[name] = component
    
    def set_metadata(self, key: str, value: str) -> None:
        self._metadata[key] = value
    
    def get_component(self, name: str) -> Optional[Any]:
        return self._components.get(name)
    
    def validate(self) -> bool:
        required = ['engine', 'chassis', 'wheels']
        return all(comp in self._components for comp in required)
    
    def __str__(self) -> str:
        specs = ", ".join(f"{k}: {v}" for k, v in self._components.items())
        meta = ", ".join(f"{k}={v}" for k, v in self._metadata.items())
        return f"Product({specs}) [{meta}]"

class VehicleAssembler(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self._product = Product()
    
    @abstractmethod
    def create_engine(self, specs: str) -> 'VehicleAssembler':
        pass
    
    @abstractmethod
    def create_chassis(self, material: str) -> 'VehicleAssembler':
        pass
    
    @abstractmethod
    def create_wheels(self, count: int) -> 'VehicleAssembler':
        pass
    
    def add_extras(self, features: Dict[str, Any]) -> 'VehicleAssembler':
        for name, feature in features.items():
            self._product.add_component(name, feature)
        return self
    
    def finalize(self) -> Product:
        if not self._product.validate():
            raise RuntimeError("Product validation failed - missing required components")
        result = self._product
        self.reset()
        return result

class CarAssembler(VehicleAssembler):
    def create_engine(self, specs: str) -> 'CarAssembler':
        self._product.add_component('engine', f"Car Engine: {specs}")
        self._product.set_metadata('type', 'automobile')
        return self
    
    def create_chassis(self, material: str) -> 'CarAssembler':
        self._product.add_component('chassis', f"Steel Chassis ({material})")
        return self
    
    def create_wheels(self, count: int = 4) -> 'CarAssembler':
        if count != 4:
            raise ValueError("Cars must have exactly 4 wheels")
        self._product.add_component('wheels', f"{count} alloy wheels")
        return self

class MotorcycleAssembler(VehicleAssembler):
    def create_engine(self, specs: str) -> 'MotorcycleAssembler':
        self._product.add_component('engine', f"Motorcycle Engine: {specs}")
        self._product.set_metadata('type', 'motorcycle')
        return self
    
    def create_chassis(self, material: str) -> 'MotorcycleAssembler':
        self._product.add_component('chassis', f"Lightweight Frame ({material})")
        return self
    
    def create_wheels(self, count: int = 2) -> 'MotorcycleAssembler':
        if count != 2:
            raise ValueError("Motorcycles must have exactly 2 wheels")
        self._product.add_component('wheels', f"{count} sport wheels")
        return self

class ProductionDirector:
    def __init__(self, assembler: VehicleAssembler):
        self._assembler = assembler
    
    def create_standard_vehicle(self) -> Product:
        return (self._assembler
                .create_engine("2.0L Turbo")
                .create_chassis("reinforced steel")
                .create_wheels()
                .finalize())
    
    def create_luxury_vehicle(self) -> Product:
        extras = {"interior": "leather", "sound_system": "premium", "navigation": "GPS"}
        return (self._assembler
                .create_engine("3.5L V6")
                .create_chassis("carbon fiber")
                .create_wheels()
                .add_extras(extras)
                .finalize())

if __name__ == "__main__":
    car_assembler = CarAssembler()
    bike_assembler = MotorcycleAssembler()
    
    car_director = ProductionDirector(car_assembler)
    bike_director = ProductionDirector(bike_assembler)
    
    standard_car = car_director.create_standard_vehicle()
    luxury_car = car_director.create_luxury_vehicle()
    standard_bike = bike_director.create_standard_vehicle()
    
    print(f"Standard Car: {standard_car}")
    print(f"Luxury Car: {luxury_car}")
    print(f"Standard Bike: {standard_bike}")
    
    custom_car = (CarAssembler()
                  .create_engine("Electric 400HP")
                  .create_chassis("aluminum")
                  .create_wheels(4)
                  .add_extras({"autopilot": "Level 3", "battery": "100kWh"})
                  .finalize())
    print(f"Custom Car: {custom_car}")