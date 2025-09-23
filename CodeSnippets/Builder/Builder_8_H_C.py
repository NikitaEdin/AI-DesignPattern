from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import copy

class Product:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._metadata: Dict[str, str] = {}
    
    def add_component(self, name: str, component: Any) -> None:
        if not name or component is None:
            raise ValueError("Component name and value cannot be empty")
        self._components[name] = copy.deepcopy(component)
    
    def set_metadata(self, key: str, value: str) -> None:
        self._metadata[key] = value
    
    def get_component(self, name: str) -> Any:
        return self._components.get(name)
    
    def validate(self) -> bool:
        required = ['engine', 'body', 'wheels']
        return all(comp in self._components for comp in required)
    
    def __str__(self) -> str:
        parts = [f"{k}: {v}" for k, v in self._components.items()]
        meta = [f"{k}={v}" for k, v in self._metadata.items()]
        return f"Product({', '.join(parts)}) [{', '.join(meta)}]"

class AbstractConstructor(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self._product = Product()
    
    @property
    def product(self) -> Product:
        result = self._product
        self.reset()
        return result
    
    @abstractmethod
    def create_engine(self, specs: Dict[str, Any]) -> 'AbstractConstructor':
        pass
    
    @abstractmethod
    def create_body(self, material: str, color: str) -> 'AbstractConstructor':
        pass
    
    @abstractmethod
    def create_wheels(self, count: int, size: str) -> 'AbstractConstructor':
        pass

class VehicleConstructor(AbstractConstructor):
    def create_engine(self, specs: Dict[str, Any]) -> 'VehicleConstructor':
        engine_data = {
            'power': specs.get('power', 100),
            'fuel_type': specs.get('fuel_type', 'gasoline'),
            'cylinders': specs.get('cylinders', 4)
        }
        self._product.add_component('engine', engine_data)
        return self
    
    def create_body(self, material: str, color: str) -> 'VehicleConstructor':
        body_data = {'material': material, 'color': color}
        self._product.add_component('body', body_data)
        return self
    
    def create_wheels(self, count: int, size: str) -> 'VehicleConstructor':
        if count <= 0:
            raise ValueError("Wheel count must be positive")
        wheels_data = {'count': count, 'size': size}
        self._product.add_component('wheels', wheels_data)
        return self
    
    def add_optional_feature(self, feature: str, config: Dict[str, Any]) -> 'VehicleConstructor':
        self._product.add_component(feature, config)
        return self
    
    def set_brand(self, brand: str) -> 'VehicleConstructor':
        self._product.set_metadata('brand', brand)
        return self

class ProductionManager:
    def __init__(self, constructor: AbstractConstructor):
        self._constructor = constructor
    
    def create_sports_car(self) -> Product:
        return (self._constructor
                .create_engine({'power': 400, 'fuel_type': 'premium', 'cylinders': 8})
                .create_body('carbon_fiber', 'red')
                .create_wheels(4, '18inch')
                .add_optional_feature('turbo', {'boost': 'high'})
                .set_brand('SportsCorp')
                .product)
    
    def create_truck(self) -> Product:
        return (self._constructor
                .create_engine({'power': 300, 'fuel_type': 'diesel', 'cylinders': 6})
                .create_body('steel', 'blue')
                .create_wheels(6, '20inch')
                .add_optional_feature('cargo_bed', {'capacity': '2000kg'})
                .set_brand('HeavyDuty')
                .product)

if __name__ == "__main__":
    constructor = VehicleConstructor()
    manager = ProductionManager(constructor)
    
    sports_car = manager.create_sports_car()
    print(f"Sports Car Valid: {sports_car.validate()}")
    print(sports_car)
    
    truck = manager.create_truck()
    print(f"\nTruck Valid: {truck.validate()}")
    print(truck)
    
    custom_vehicle = (VehicleConstructor()
                     .create_engine({'power': 150, 'fuel_type': 'electric'})
                     .create_body('aluminum', 'green')
                     .create_wheels(4, '16inch')
                     .set_brand('EcoCorp')
                     .product)
    
    print(f"\nCustom Vehicle Valid: {custom_vehicle.validate()}")
    print(custom_vehicle)