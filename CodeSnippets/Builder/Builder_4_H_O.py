from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import threading
import time

@dataclass(frozen=True)
class Computer:
    cpu: str
    ram_gb: int
    storage_gb: int
    gpu: Optional[str]
    os: str
    extras: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.cpu or not isinstance(self.cpu, str):
            raise ValueError("cpu must be a non-empty string")
        if not isinstance(self.ram_gb, int) or self.ram_gb <= 0:
            raise ValueError("ram_gb must be a positive integer")
        if not isinstance(self.storage_gb, int) or self.storage_gb <= 0:
            raise ValueError("storage_gb must be a positive integer")
        object.__setattr__(self, "extras", dict(self.extras))

class Configurator(ABC):
    @abstractmethod
    def reset(self) -> Configurator: ...
    @abstractmethod
    def set_cpu(self, cpu: str) -> Configurator: ...
    @abstractmethod
    def set_ram(self, gb: int) -> Configurator: ...
    @abstractmethod
    def set_storage(self, gb: int) -> Configurator: ...
    @abstractmethod
    def set_gpu(self, gpu: Optional[str]) -> Configurator: ...
    @abstractmethod
    def set_os(self, os: str) -> Configurator: ...
    @abstractmethod
    def add_extra(self, key: str, value: Any) -> Configurator: ...
    @abstractmethod
    def assemble(self) -> Computer: ...

class Assembler(Configurator):
    def __init__(self):
        self._lock = threading.RLock()
        self._state: Dict[str, Any] = {}
        self._last_product: Optional[Computer] = None
        self.reset()

    def reset(self) -> Assembler:
        with self._lock:
            self._state = {"cpu": None, "ram_gb": None, "storage_gb": None, "gpu": None, "os": "Linux", "extras": {}}
            return self

    def set_cpu(self, cpu: str) -> Assembler:
        if not cpu or not isinstance(cpu, str):
            raise ValueError("cpu must be a non-empty string")
        with self._lock:
            self._state["cpu"] = cpu
            return self

    def set_ram(self, gb: int) -> Assembler:
        if not isinstance(gb, int) or gb <= 0:
            raise ValueError("ram must be a positive integer")
        with self._lock:
            self._state["ram_gb"] = gb
            return self

    def set_storage(self, gb: int) -> Assembler:
        if not isinstance(gb, int) or gb <= 0:
            raise ValueError("storage must be a positive integer")
        with self._lock:
            self._state["storage_gb"] = gb
            return self

    def set_gpu(self, gpu: Optional[str]) -> Assembler:
        with self._lock:
            self._state["gpu"] = gpu
            return self

    def set_os(self, os: str) -> Assembler:
        if not os or not isinstance(os, str):
            raise ValueError("os must be a non-empty string")
        with self._lock:
            self._state["os"] = os
            return self

    def add_extra(self, key: str, value: Any) -> Assembler:
        if not key:
            raise ValueError("extra key must be non-empty")
        with self._lock:
            self._state["extras"][key] = value
            return self

    def assemble(self) -> Computer:
        with self._lock:
            missing = [k for k in ("cpu", "ram_gb", "storage_gb") if not self._state.get(k)]
            if missing:
                raise ValueError(f"Cannot assemble, missing fields: {missing}")
            product = Computer(
                cpu=self._state["cpu"],
                ram_gb=self._state["ram_gb"],
                storage_gb=self._state["storage_gb"],
                gpu=self._state["gpu"],
                os=self._state["os"],
                extras=dict(self._state["extras"]),
            )
            self._last_product = product
            return product

    def resume_from(self, product: Computer) -> Assembler:
        if not isinstance(product, Computer):
            raise ValueError("resume_from requires a Computer instance")
        with self._lock:
            self._state.update({
                "cpu": product.cpu,
                "ram_gb": product.ram_gb,
                "storage_gb": product.storage_gb,
                "gpu": product.gpu,
                "os": product.os,
                "extras": dict(product.extras),
            })
            return self

class Orchestrator:
    def prepare_gaming(self, assembler: Configurator) -> Computer:
        return (assembler.reset()
                .set_cpu("Intel i9-13900K")
                .set_ram(32)
                .set_storage(2000)
                .set_gpu("NVIDIA RTX 4090")
                .set_os("Windows 11")
                .add_extra("cooling", "liquid")
                .assemble())

    def prepare_office(self, assembler: Configurator) -> Computer:
        return (assembler.reset()
                .set_cpu("Intel i5-12400")
                .set_ram(16)
                .set_storage(512)
                .set_gpu(None)
                .set_os("Windows 11 Pro")
                .add_extra("warranty", "3 years")
                .assemble())

    def prepare_minimal(self, assembler: Configurator) -> Computer:
        return (assembler.reset()
                .set_cpu("ARM Cortex-A78")
                .set_ram(4)
                .set_storage(128)
                .set_gpu(None)
                .assemble())

if __name__ == "__main__":
    assembler = Assembler()
    orchestrator = Orchestrator()

    gaming_pc = orchestrator.prepare_gaming(assembler)
    print("Gaming PC:", gaming_pc)

    office_pc = orchestrator.prepare_office(assembler)
    print("Office PC:", office_pc)

    try:
        incomplete = assembler.reset().set_cpu("Test CPU").assemble()
    except ValueError as e:
        print("Expected error for incomplete config:", e)

    base = orchestrator.prepare_office(assembler)
    modified_pc = assembler.resume_from(base).set_ram(32).add_extra("ssd_cache", True).assemble()
    print("Modified from office:", modified_pc)