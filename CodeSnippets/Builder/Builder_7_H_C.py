from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from functools import wraps

def validate_step(step_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, '_completed_steps') and step_name in self._completed_steps:
                raise ValueError(f"Step '{step_name}' has already been completed")
            result = func(self, *args, **kwargs)
            if not hasattr(self, '_completed_steps'):
                self._completed_steps = set()
            self._completed_steps.add(step_name)
            return result
        return wrapper
    return decorator

class Computer:
    def __init__(self):
        self.cpu: Optional[str] = None
        self.ram: Optional[str] = None
        self.storage: Optional[str] = None
        self.gpu: Optional[str] = None
        self.case: Optional[str] = None
        self.cooling: Optional[str] = None
        self._extras: Dict[str, Any] = {}
    
    def add_extra(self, key: str, value: Any):
        self._extras[key] = value
    
    def get_specs(self) -> Dict[str, Any]:
        specs = {
            'cpu': self.cpu,
            'ram': self.ram,
            'storage': self.storage,
            'gpu': self.gpu,
            'case': self.case,
            'cooling': self.cooling
        }
        specs.update(self._extras)
        return {k: v for k, v in specs.items() if v is not None}

class ComputerAssembler(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._computer = Computer()
        self._completed_steps = set()
        return self
    
    @abstractmethod
    def set_cpu(self, cpu: str): pass
    
    @abstractmethod
    def set_memory(self, ram: str): pass
    
    @abstractmethod
    def set_storage(self, storage: str): pass
    
    def set_graphics(self, gpu: str):
        self._computer.gpu = gpu
        return self
    
    def set_case(self, case: str):
        self._computer.case = case
        return self
    
    def finalize(self) -> Computer:
        required_steps = {'cpu', 'memory', 'storage'}
        missing_steps = required_steps - self._completed_steps
        if missing_steps:
            raise ValueError(f"Missing required steps: {missing_steps}")
        
        result = self._computer
        self.reset()
        return result

class GamingRig(ComputerAssembler):
    @validate_step('cpu')
    def set_cpu(self, cpu: str):
        if 'i3' in cpu.lower() or 'ryzen 3' in cpu.lower():
            raise ValueError("Gaming rigs require high-performance CPUs")
        self._computer.cpu = cpu
        self._computer.cooling = "Liquid Cooling"
        return self
    
    @validate_step('memory')
    def set_memory(self, ram: str):
        ram_size = int(''.join(filter(str.isdigit, ram)))
        if ram_size < 16:
            raise ValueError("Gaming rigs require at least 16GB RAM")
        self._computer.ram = ram
        return self
    
    @validate_step('storage')
    def set_storage(self, storage: str):
        if 'hdd' in storage.lower():
            self._computer.storage = f"SSD + {storage}"
        else:
            self._computer.storage = storage
        return self

class OfficeWorkstation(ComputerAssembler):
    @validate_step('cpu')
    def set_cpu(self, cpu: str):
        self._computer.cpu = cpu
        self._computer.cooling = "Stock Cooling"
        return self
    
    @validate_step('memory')
    def set_memory(self, ram: str):
        self._computer.ram = ram
        return self
    
    @validate_step('storage')
    def set_storage(self, storage: str):
        self._computer.storage = storage
        self._computer.add_extra('warranty', '3 years')
        return self

class ComputerEngineer:
    def __init__(self, assembler: ComputerAssembler):
        self._assembler = assembler
    
    def switch_assembler(self, assembler: ComputerAssembler):
        self._assembler = assembler
    
    def build_basic_config(self, cpu: str, ram: str, storage: str) -> Computer:
        return (self._assembler
                .reset()
                .set_cpu(cpu)
                .set_memory(ram)
                .set_storage(storage)
                .finalize())
    
    def build_complete_config(self, specs: Dict[str, str]) -> Computer:
        self._assembler.reset()
        self._assembler.set_cpu(specs['cpu'])
        self._assembler.set_memory(specs['ram'])
        self._assembler.set_storage(specs['storage'])
        
        if 'gpu' in specs:
            self._assembler.set_graphics(specs['gpu'])
        if 'case' in specs:
            self._assembler.set_case(specs['case'])
        
        return self._assembler.finalize()

if __name__ == "__main__":
    engineer = ComputerEngineer(GamingRig())
    
    gaming_pc = engineer.build_basic_config("Intel i7-13700K", "32GB DDR5", "1TB NVMe SSD")
    print("Gaming PC:", gaming_pc.get_specs())
    
    engineer.switch_assembler(OfficeWorkstation())
    office_pc = engineer.build_complete_config({
        'cpu': 'Intel i5-13400',
        'ram': '16GB DDR4',
        'storage': '512GB SSD',
        'case': 'Mini ITX'
    })
    print("Office PC:", office_pc.get_specs())
    
    try:
        gaming_rig = GamingRig()
        gaming_rig.set_cpu("Intel i3-12100").set_cpu("Intel i7-13700K")
    except ValueError as e:
        print("Error:", e)