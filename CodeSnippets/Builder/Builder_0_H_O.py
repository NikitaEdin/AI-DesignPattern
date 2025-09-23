from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any
from abc import ABC, abstractmethod


class AssemblyError(Exception):
    pass


@dataclass(frozen=True)
class ComputerSystem:
    cpu: str
    ram_gb: int
    storage_gb: int
    gpu: Optional[str]
    os: str
    extras: Tuple[str, ...] = field(default_factory=tuple)


class Specification(ABC):
    @abstractmethod
    def set_cpu(self, cpu: str) -> "Specification":
        pass

    @abstractmethod
    def set_ram(self, gb: int) -> "Specification":
        pass

    @abstractmethod
    def set_storage(self, gb: int) -> "Specification":
        pass

    @abstractmethod
    def set_gpu(self, gpu: Optional[str]) -> "Specification":
        pass

    @abstractmethod
    def set_os(self, os: str) -> "Specification":
        pass

    @abstractmethod
    def add_extra(self, item: str) -> "Specification":
        pass

    @abstractmethod
    def finalize(self, reset_after: bool = True) -> ComputerSystem:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


class LaptopAssembler(Specification):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._parts: Dict[str, Any] = {
            "cpu": None,
            "ram_gb": None,
            "storage_gb": None,
            "gpu": None,
            "os": None,
            "extras": []
        }
        self._product_cache: Optional[ComputerSystem] = None

    def set_cpu(self, cpu: str) -> "LaptopAssembler":
        if not cpu or not isinstance(cpu, str):
            raise AssemblyError("cpu must be a non-empty string")
        self._parts["cpu"] = cpu
        self._product_cache = None
        return self

    def set_ram(self, gb: int) -> "LaptopAssembler":
        if not isinstance(gb, int) or gb <= 0:
            raise AssemblyError("ram_gb must be a positive integer")
        self._parts["ram_gb"] = gb
        self._product_cache = None
        return self

    def set_storage(self, gb: int) -> "LaptopAssembler":
        if not isinstance(gb, int) or gb <= 0:
            raise AssemblyError("storage_gb must be a positive integer")
        self._parts["storage_gb"] = gb
        self._product_cache = None
        return self

    def set_gpu(self, gpu: Optional[str]) -> "LaptopAssembler":
        if gpu is not None and not isinstance(gpu, str):
            raise AssemblyError("gpu must be a string or None")
        self._parts["gpu"] = gpu
        self._product_cache = None
        return self

    def set_os(self, os: str) -> "LaptopAssembler":
        if not os or not isinstance(os, str):
            raise AssemblyError("os must be a non-empty string")
        self._parts["os"] = os
        self._product_cache = None
        return self

    def add_extra(self, item: str) -> "LaptopAssembler":
        if not item or not isinstance(item, str):
            raise AssemblyError("extra must be a non-empty string")
        if item not in self._parts["extras"]:
            self._parts["extras"].append(item)
        self._product_cache = None
        return self

    def _validate(self) -> None:
        required = ["cpu", "ram_gb", "storage_gb", "os"]
        missing = [k for k in required if not self._parts.get(k)]
        if missing:
            raise AssemblyError(f"Missing required components: {', '.join(missing)}")
        gpu = self._parts.get("gpu")
        extras = set(self._parts.get("extras", []))
        if gpu and ("RTX" in gpu or "RX" in gpu) and "High-Watt PSU" not in extras:
            raise AssemblyError("High-performance GPU requires 'High-Watt PSU' in extras")
        if self._parts["ram_gb"] > 128:
            raise AssemblyError("RAM exceeds supported maximum")

    def finalize(self, reset_after: bool = True) -> ComputerSystem:
        if self._product_cache is not None:
            product = self._product_cache
        else:
            self._validate()
            extras = tuple(sorted(set(self._parts["extras"])))
            product = ComputerSystem(
                cpu=str(self._parts["cpu"]),
                ram_gb=int(self._parts["ram_gb"]),
                storage_gb=int(self._parts["storage_gb"]),
                gpu=self._parts["gpu"],
                os=str(self._parts["os"]),
                extras=extras
            )
            self._product_cache = product
        if reset_after:
            self.reset()
        return product


class Orchestrator:
    def __init__(self, spec: Specification) -> None:
        self.spec = spec

    def assemble_gaming(self) -> ComputerSystem:
        return (
            self.spec.set_cpu("Intel i9")
            .set_ram(32)
            .set_storage(2000)
            .set_gpu("NVIDIA RTX 4080")
            .set_os("Windows 11")
            .add_extra("High-Watt PSU")
            .add_extra("Advanced Cooling")
            .finalize()
        )

    def assemble_ultraportable(self) -> ComputerSystem:
        return (
            self.spec.set_cpu("Intel i7-L")
            .set_ram(16)
            .set_storage(512)
            .set_gpu(None)
            .set_os("Windows 11 Home")
            .add_extra("Extended Battery")
            .finalize()
        )

    def assemble_minimal(self) -> ComputerSystem:
        return (
            self.spec.set_cpu("ARM N1")
            .set_ram(8)
            .set_storage(128)
            .set_gpu(None)
            .set_os("Linux")
            .finalize()
        )


if __name__ == "__main__":
    assembler = LaptopAssembler()
    orchestrator = Orchestrator(assembler)
    gaming = orchestrator.assemble_gaming()
    ultraportable = orchestrator.assemble_ultraportable()
    manual = (
        assembler.set_cpu("Custom CPU")
        .set_ram(64)
        .set_storage(1000)
        .set_gpu("AMD RX 7900")
        .set_os("Windows 11 Pro")
        .add_extra("High-Watt PSU")
        .finalize(reset_after=False)
    )
    reused = assembler.finalize()
    print(gaming)
    print(ultraportable)
    print(manual)
    print(reused)