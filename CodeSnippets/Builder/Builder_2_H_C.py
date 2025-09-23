from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Product:
    def __init__(self):
        self._components = {}
    
    def add_component(self, name: str, value: Any) -> None:
        self._components[name] = value
    
    def get_component(self, name: str) -> Any:
        return self._components.get(name)
    
    def validate(self) -> bool:
        required = {'engine', 'wheels', 'body'}
        return all(comp in self._components for comp in required)
    
    def __str__(self) -> str:
        return f"Vehicle: {', '.join(f'{k}={v}' for k, v in self._components.items())}"

class AbstractAssembler(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self._product = Product()
    
    @abstractmethod
    def set_engine(self, engine_type: str) -> 'AbstractAssembler':
        pass
    
    @abstractmethod
    def set_wheels(self, wheel_count: int) -> 'AbstractAssembler':
        pass
    
    @abstractmethod
    def set_body(self, body_type: str) -> 'AbstractAssembler':
        pass
    
    def add_feature(self, name: str, value: Any) -> 'AbstractAssembler':
        self._product.add_component(name, value)
        return self
    
    def get_result(self) -> Product:
        if not self._product.validate():
            raise ValueError("Product incomplete: missing required components")
        result = self._product
        self.reset()
        return result

class CarAssembler(AbstractAssembler):
    def set_engine(self, engine_type: str) -> 'CarAssembler':
        valid_engines = {'v4', 'v6', 'v8', 'electric'}
        if engine_type not in valid_engines:
            raise ValueError(f"Invalid engine type. Must be one of {valid_engines}")
        self._product.add_component('engine', f"{engine_type}_engine")
        return self
    
    def set_wheels(self, wheel_count: int) -> 'CarAssembler':
        if wheel_count not in [4]:
            raise ValueError("Cars must have exactly 4 wheels")
        self._product.add_component('wheels', wheel_count)
        return self
    
    def set_body(self, body_type: str) -> 'CarAssembler':
        valid_bodies = {'sedan', 'hatchback', 'suv', 'coupe'}
        if body_type not in valid_bodies:
            raise ValueError(f"Invalid body type. Must be one of {valid_bodies}")
        self._product.add_component('body', f"{body_type}_body")
        return self

class MotorcycleAssembler(AbstractAssembler):
    def set_engine(self, engine_type: str) -> 'MotorcycleAssembler':
        valid_engines = {'single', 'twin', 'electric'}
        if engine_type not in valid_engines:
            raise ValueError(f"Invalid engine type. Must be one of {valid_engines}")
        self._product.add_component('engine', f"{engine_type}_engine")
        return self
    
    def set_wheels(self, wheel_count: int) -> 'MotorcycleAssembler':
        if wheel_count not in [2, 3]:
            raise ValueError("Motorcycles must have 2 or 3 wheels")
        self._product.add_component('wheels', wheel_count)
        return self
    
    def set_body(self, body_type: str) -> 'MotorcycleAssembler':
        valid_bodies = {'sport', 'cruiser', 'touring', 'dirt'}
        if body_type not in valid_bodies:
            raise ValueError(f"Invalid body type. Must be one of {valid_bodies}")
        self._product.add_component('body', f"{body_type}_body")
        return self

class Director:
    def __init__(self, assembler: AbstractAssembler):
        self._assembler = assembler
    
    def construct_luxury_car(self) -> Product:
        return (self._assembler
                .set_engine('v8')
                .set_wheels(4)
                .set_body('sedan')
                .add_feature('leather_seats', True)
                .add_feature('gps', True)
                .get_result())
    
    def construct_sport_bike(self) -> Product:
        return (self._assembler
                .set_engine('twin')
                .set_wheels(2)
                .set_body('sport')
                .add_feature('abs', True)
                .get_result())

if __name__ == "__main__":
    car_assembler = CarAssembler()
    motorcycle_assembler = MotorcycleAssembler()
    
    director = Director(car_assembler)
    luxury_car = director.construct_luxury_car()
    print(luxury_car)
    
    director = Director(motorcycle_assembler)
    sport_bike = director.construct_sport_bike()
    print(sport_bike)
    
    custom_car = (CarAssembler()
                  .set_engine('electric')
                  .set_wheels(4)
                  .set_body('hatchback')
                  .add_feature('autopilot', True)
                  .get_result())
    print(custom_car)