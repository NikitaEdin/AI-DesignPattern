from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Product:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._metadata: Dict[str, str] = {}
    
    def add_component(self, name: str, value: Any) -> None:
        if not name or value is None:
            raise ValueError("Component name and value cannot be empty")
        self._components[name] = value
    
    def add_metadata(self, key: str, value: str) -> None:
        self._metadata[key] = value
    
    def get_component(self, name: str) -> Optional[Any]:
        return self._components.get(name)
    
    def validate(self) -> bool:
        required = ['engine', 'wheels', 'body']
        return all(comp in self._components for comp in required)
    
    def serialize(self) -> str:
        return json.dumps({
            'components': self._components,
            'metadata': self._metadata
        }, indent=2)

class Assembler(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self._product = Product()
    
    @abstractmethod
    def add_engine(self, engine_type: str) -> 'Assembler':
        pass
    
    @abstractmethod
    def add_wheels(self, count: int, wheel_type: str) -> 'Assembler':
        pass
    
    @abstractmethod
    def add_body(self, material: str, color: str) -> 'Assembler':
        pass
    
    def add_extras(self, extras: Dict[str, Any]) -> 'Assembler':
        for name, value in extras.items():
            self._product.add_component(f"extra_{name}", value)
        return self
    
    def finalize(self) -> Product:
        if not self._product.validate():
            raise RuntimeError("Product is incomplete - missing required components")
        result = self._product
        self.reset()
        return result

class VehicleAssembler(Assembler):
    def add_engine(self, engine_type: str) -> 'VehicleAssembler':
        engine_specs = {
            'v4': {'power': 150, 'efficiency': 8.5},
            'v6': {'power': 250, 'efficiency': 6.2},
            'electric': {'power': 300, 'efficiency': 12.0}
        }
        
        if engine_type not in engine_specs:
            raise ValueError(f"Unsupported engine type: {engine_type}")
        
        self._product.add_component('engine', {
            'type': engine_type,
            **engine_specs[engine_type]
        })
        self._product.add_metadata('engine_installed', 'true')
        return self
    
    def add_wheels(self, count: int, wheel_type: str = 'standard') -> 'VehicleAssembler':
        if count not in [2, 4, 6, 8]:
            raise ValueError("Invalid wheel count")
        
        self._product.add_component('wheels', {
            'count': count,
            'type': wheel_type,
            'diameter': 18 if wheel_type == 'sport' else 16
        })
        return self
    
    def add_body(self, material: str, color: str) -> 'VehicleAssembler':
        valid_materials = ['steel', 'aluminum', 'carbon_fiber']
        if material not in valid_materials:
            raise ValueError(f"Invalid material: {material}")
        
        self._product.add_component('body', {
            'material': material,
            'color': color,
            'weight': {'steel': 1500, 'aluminum': 1200, 'carbon_fiber': 900}[material]
        })
        return self

class Director:
    def __init__(self, assembler: Assembler):
        self._assembler = assembler
    
    def create_sports_car(self) -> Product:
        return (self._assembler
                .add_engine('v6')
                .add_wheels(4, 'sport')
                .add_body('carbon_fiber', 'red')
                .add_extras({'sunroof': True, 'sound_system': 'premium'})
                .finalize())
    
    def create_eco_vehicle(self) -> Product:
        return (self._assembler
                .add_engine('electric')
                .add_wheels(4, 'standard')
                .add_body('aluminum', 'white')
                .add_extras({'solar_panel': True, 'regenerative_braking': True})
                .finalize())

if __name__ == "__main__":
    assembler = VehicleAssembler()
    director = Director(assembler)
    
    sports_car = director.create_sports_car()
    print("Sports Car Configuration:")
    print(sports_car.serialize())
    print()
    
    eco_car = director.create_eco_vehicle()
    print("Eco Vehicle Configuration:")
    print(eco_car.serialize())
    print()
    
    custom_vehicle = (VehicleAssembler()
                     .add_engine('v4')
                     .add_wheels(6, 'standard')
                     .add_body('steel', 'blue')
                     .finalize())
    
    print(f"Custom vehicle engine power: {custom_vehicle.get_component('engine')['power']} HP")