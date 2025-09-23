from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json

class Product:
    def __init__(self):
        self._parts: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}
    
    def add_part(self, name: str, value: Any) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Part name must be a non-empty string")
        self._parts[name] = value
    
    def set_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value
    
    def get_part(self, name: str) -> Any:
        return self._parts.get(name)
    
    def validate(self) -> bool:
        required_parts = self._metadata.get('required_parts', [])
        return all(part in self._parts for part in required_parts)
    
    def serialize(self) -> str:
        return json.dumps({
            'parts': self._parts,
            'metadata': self._metadata
        }, default=str, indent=2)
    
    def __str__(self) -> str:
        parts_str = ', '.join(f"{k}: {v}" for k, v in self._parts.items())
        return f"Product({parts_str})"

class Assembler(ABC):
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
    def add_core_component(self, spec: str) -> 'Assembler':
        pass
    
    @abstractmethod
    def add_peripheral(self, peripheral_type: str, config: Dict[str, Any]) -> 'Assembler':
        pass
    
    @abstractmethod
    def configure_settings(self, settings: Dict[str, Any]) -> 'Assembler':
        pass

class ComputerAssembler(Assembler):
    def add_core_component(self, spec: str) -> 'ComputerAssembler':
        if not spec:
            raise ValueError("Component specification cannot be empty")
        self._product.add_part('processor', spec)
        self._product.add_part('memory', f"{spec}_compatible_ram")
        return self
    
    def add_peripheral(self, peripheral_type: str, config: Dict[str, Any]) -> 'ComputerAssembler':
        peripherals = self._product.get_part('peripherals') or []
        peripherals.append({
            'type': peripheral_type,
            'config': config,
            'id': len(peripherals)
        })
        self._product.add_part('peripherals', peripherals)
        return self
    
    def configure_settings(self, settings: Dict[str, Any]) -> 'ComputerAssembler':
        current_settings = self._product.get_part('settings') or {}
        current_settings.update(settings)
        self._product.add_part('settings', current_settings)
        return self
    
    def add_storage(self, storage_type: str, capacity: str) -> 'ComputerAssembler':
        storage_devices = self._product.get_part('storage') or []
        storage_devices.append({'type': storage_type, 'capacity': capacity})
        self._product.add_part('storage', storage_devices)
        return self

class VehicleAssembler(Assembler):
    def add_core_component(self, spec: str) -> 'VehicleAssembler':
        self._product.add_part('engine', spec)
        self._product.set_metadata('required_parts', ['engine', 'wheels'])
        return self
    
    def add_peripheral(self, peripheral_type: str, config: Dict[str, Any]) -> 'VehicleAssembler':
        if peripheral_type == 'wheels':
            self._product.add_part('wheels', config)
        else:
            accessories = self._product.get_part('accessories') or []
            accessories.append({'type': peripheral_type, 'config': config})
            self._product.add_part('accessories', accessories)
        return self
    
    def configure_settings(self, settings: Dict[str, Any]) -> 'VehicleAssembler':
        self._product.add_part('configuration', settings)
        return self

class Director:
    def __init__(self, assembler: Assembler):
        self._assembler = assembler
    
    def construct_gaming_computer(self) -> Product:
        return (self._assembler
                .add_core_component('Intel i9-13900K')
                .add_peripheral('graphics_card', {'model': 'RTX 4080', 'memory': '16GB'})
                .add_peripheral('monitor', {'size': '27inch', 'resolution': '4K'})
                .configure_settings({'overclocking': True, 'rgb_lighting': True})
                .product)
    
    def construct_sports_car(self) -> Product:
        return (self._assembler
                .add_core_component('V8_Twin_Turbo')
                .add_peripheral('wheels', {'type': 'racing', 'size': '20inch'})
                .add_peripheral('spoiler', {'material': 'carbon_fiber', 'adjustable': True})
                .configure_settings({'suspension': 'sport', 'exhaust': 'performance'})
                .product)

if __name__ == "__main__":
    computer_assembler = ComputerAssembler()
    director = Director(computer_assembler)
    
    gaming_pc = director.construct_gaming_computer()
    print("Gaming Computer:", gaming_pc)
    print("Valid:", gaming_pc.validate())
    
    custom_pc = (ComputerAssembler()
                 .add_core_component('AMD Ryzen 7')
                 .add_storage('SSD', '1TB')
                 .add_storage('HDD', '2TB')
                 .configure_settings({'quiet_mode': True})
                 .product)
    print("\nCustom Computer:", custom_pc)
    
    vehicle_assembler = VehicleAssembler()
    director = Director(vehicle_assembler)
    
    sports_car = director.construct_sports_car()
    print("\nSports Car:", sports_car)
    print("Valid:", sports_car.validate())