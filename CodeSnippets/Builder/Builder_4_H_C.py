from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from functools import wraps

def validate_step(step_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if step_name in self._completed_steps:
                raise ValueError(f"Step '{step_name}' already completed")
            result = func(self, *args, **kwargs)
            self._completed_steps.add(step_name)
            return result
        return wrapper
    return decorator

class Computer:
    def __init__(self):
        self.cpu: Optional[str] = None
        self.memory: Optional[int] = None
        self.storage: Optional[str] = None
        self.graphics: Optional[str] = None
        self.components: List[str] = []
        self.warranty: Optional[int] = None
    
    def __str__(self):
        specs = [f"CPU: {self.cpu}", f"Memory: {self.memory}GB", 
                f"Storage: {self.storage}", f"Graphics: {self.graphics}"]
        if self.components:
            specs.append(f"Components: {', '.join(self.components)}")
        if self.warranty:
            specs.append(f"Warranty: {self.warranty} years")
        return "Computer(" + ", ".join(specs) + ")"

class ConfigurationAssistant(ABC):
    def __init__(self):
        self._computer = Computer()
        self._completed_steps = set()
        self._required_steps = {"cpu", "memory", "storage"}
    
    def reset(self):
        self._computer = Computer()
        self._completed_steps.clear()
        return self
    
    @abstractmethod
    def configure_processor(self, cpu_type: str):
        pass
    
    @abstractmethod
    def configure_memory(self, size_gb: int):
        pass
    
    @abstractmethod
    def configure_storage(self, storage_type: str):
        pass
    
    def add_component(self, component: str):
        self._computer.components.append(component)
        return self
    
    def set_warranty(self, years: int):
        if years < 1 or years > 10:
            raise ValueError("Warranty must be between 1 and 10 years")
        self._computer.warranty = years
        return self
    
    def finalize(self):
        missing_steps = self._required_steps - self._completed_steps
        if missing_steps:
            raise ValueError(f"Missing required configurations: {missing_steps}")
        return self._computer

class GamingAssistant(ConfigurationAssistant):
    @validate_step("cpu")
    def configure_processor(self, cpu_type: str):
        gaming_cpus = {"intel_i9", "amd_ryzen9", "intel_i7", "amd_ryzen7"}
        if cpu_type not in gaming_cpus:
            raise ValueError(f"Invalid gaming CPU. Choose from: {gaming_cpus}")
        self._computer.cpu = cpu_type
        return self
    
    @validate_step("memory")
    def configure_memory(self, size_gb: int):
        if size_gb < 16:
            raise ValueError("Gaming systems require at least 16GB RAM")
        self._computer.memory = size_gb
        return self
    
    @validate_step("storage")
    def configure_storage(self, storage_type: str):
        if not storage_type.endswith("SSD"):
            raise ValueError("Gaming systems require SSD storage")
        self._computer.storage = storage_type
        return self
    
    def configure_graphics(self, gpu: str):
        gaming_gpus = {"rtx4090", "rtx4080", "rx7900xt", "rx7800xt"}
        if gpu not in gaming_gpus:
            raise ValueError(f"Invalid gaming GPU. Choose from: {gaming_gpus}")
        self._computer.graphics = gpu
        return self

class OfficeAssistant(ConfigurationAssistant):
    @validate_step("cpu")
    def configure_processor(self, cpu_type: str):
        office_cpus = {"intel_i5", "amd_ryzen5", "intel_i3", "amd_ryzen3"}
        if cpu_type not in office_cpus:
            raise ValueError(f"Invalid office CPU. Choose from: {office_cpus}")
        self._computer.cpu = cpu_type
        return self
    
    @validate_step("memory")
    def configure_memory(self, size_gb: int):
        if size_gb < 8 or size_gb > 32:
            raise ValueError("Office systems require 8-32GB RAM")
        self._computer.memory = size_gb
        return self
    
    @validate_step("storage")
    def configure_storage(self, storage_type: str):
        self._computer.storage = storage_type
        return self
    
    def configure_graphics(self, gpu: str = "integrated"):
        self._computer.graphics = gpu
        return self

class SystemDirector:
    def __init__(self, assistant: ConfigurationAssistant):
        self._assistant = assistant
    
    def create_high_end_gaming_pc(self):
        return (self._assistant.reset()
                .configure_processor("intel_i9")
                .configure_memory(32)
                .configure_storage("2TB_NVME_SSD")
                .configure_graphics("rtx4090")
                .add_component("RGB_Cooling")
                .add_component("Mechanical_Keyboard")
                .set_warranty(3)
                .finalize())
    
    def create_standard_office_pc(self):
        return (self._assistant.reset()
                .configure_processor("intel_i5")
                .configure_memory(16)
                .configure_storage("512GB_SSD")
                .configure_graphics()
                .add_component("Wireless_Mouse")
                .set_warranty(2)
                .finalize())

if __name__ == "__main__":
    gaming_assistant = GamingAssistant()
    office_assistant = OfficeAssistant()
    
    director = SystemDirector(gaming_assistant)
    gaming_pc = director.create_high_end_gaming_pc()
    print("Gaming PC:", gaming_pc)
    
    director = SystemDirector(office_assistant)
    office_pc = director.create_standard_office_pc()
    print("Office PC:", office_pc)
    
    custom_pc = (gaming_assistant.reset()
                 .configure_processor("amd_ryzen7")
                 .configure_memory(16)
                 .configure_storage("1TB_SSD")
                 .finalize())
    print("Custom PC:", custom_pc)
    
    try:
        gaming_assistant.configure_processor("intel_i9")
    except ValueError as e:
        print(f"Validation Error: {e}")