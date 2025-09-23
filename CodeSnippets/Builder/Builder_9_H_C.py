from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Product:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._metadata: Dict[str, str] = {}
    
    def add_component(self, name: str, value: Any) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Component name must be a non-empty string")
        self._components[name] = value
    
    def add_metadata(self, key: str, value: str) -> None:
        self._metadata[key] = value
    
    def get_component(self, name: str) -> Any:
        return self._components.get(name)
    
    def validate(self) -> bool:
        required = ['engine', 'wheels', 'body']
        return all(comp in self._components for comp in required)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'components': self._components.copy(),
            'metadata': self._metadata.copy()
        }

class ConstructorInterface(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass
    
    @abstractmethod
    def set_engine(self, engine_type: str) -> 'ConstructorInterface':
        pass
    
    @abstractmethod
    def set_wheels(self, count: int) -> 'ConstructorInterface':
        pass
    
    @abstractmethod
    def set_body(self, body_type: str) -> 'ConstructorInterface':
        pass
    
    @abstractmethod
    def add_feature(self, feature: str) -> 'ConstructorInterface':
        pass
    
    @abstractmethod
    def build(self) -> Product:
        pass

class VehicleConstructor(ConstructorInterface):
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self._product = Product()
        self._features = []
    
    def set_engine(self, engine_type: str) -> 'VehicleConstructor':
        if not engine_type:
            raise ValueError("Engine type cannot be empty")
        self._product.add_component('engine', engine_type)
        return self
    
    def set_wheels(self, count: int) -> 'VehicleConstructor':
        if count <= 0:
            raise ValueError("Wheel count must be positive")
        self._product.add_component('wheels', count)
        return self
    
    def set_body(self, body_type: str) -> 'VehicleConstructor':
        if not body_type:
            raise ValueError("Body type cannot be empty")
        self._product.add_component('body', body_type)
        return self
    
    def add_feature(self, feature: str) -> 'VehicleConstructor':
        if feature and feature not in self._features:
            self._features.append(feature)
            self._product.add_component('features', self._features.copy())
        return self
    
    def build(self) -> Product:
        if not self._product.validate():
            raise RuntimeError("Product validation failed - missing required components")
        
        self._product.add_metadata('created_by', self.__class__.__name__)
        result = self._product
        self.reset()
        return result

class Director:
    def __init__(self, constructor: ConstructorInterface):
        self._constructor = constructor
    
    def make_sports_car(self) -> Product:
        return (self._constructor
                .reset()
                .set_engine('V8')
                .set_wheels(4)
                .set_body('coupe')
                .add_feature('turbo')
                .add_feature('racing_stripes')
                .build())
    
    def make_motorcycle(self) -> Product:
        return (self._constructor
                .reset()
                .set_engine('V2')
                .set_wheels(2)
                .set_body('naked')
                .add_feature('kickstand')
                .build())

if __name__ == "__main__":
    constructor = VehicleConstructor()
    director = Director(constructor)
    
    sports_car = director.make_sports_car()
    print(f"Sports car: {json.dumps(sports_car.to_dict(), indent=2)}")
    
    motorcycle = director.make_motorcycle()
    print(f"Motorcycle: {json.dumps(motorcycle.to_dict(), indent=2)}")
    
    custom_vehicle = (VehicleConstructor()
                     .set_engine('electric')
                     .set_wheels(3)
                     .set_body('trike')
                     .add_feature('solar_panel')
                     .add_feature('bluetooth')
                     .build())
    
    print(f"Custom vehicle: {json.dumps(custom_vehicle.to_dict(), indent=2)}")