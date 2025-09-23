from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
from abc import ABC, abstractmethod
from typing import List, Optional, Set


@dataclass(frozen=True)
class Product:
    name: str
    base: str
    color: str
    extras: List[str]
    version: int


class AssemblerInterface(ABC):
    @abstractmethod
    def set_name(self, name: str) -> AssemblerInterface: ...
    @abstractmethod
    def choose_base(self, base: str) -> AssemblerInterface: ...
    @abstractmethod
    def paint(self, color: str) -> AssemblerInterface: ...
    @abstractmethod
    def add_extra(self, extra: str) -> AssemblerInterface: ...
    @abstractmethod
    def set_version(self, version: int) -> AssemblerInterface: ...
    @abstractmethod
    def build(self) -> Product: ...


class StandardAssembler(AssemblerInterface):
    _COMPAT: dict = {
        "alpha": {"sunroof", "heated_seats", "sport_rims"},
        "beta": {"tow_package", "roof_rack"},
        "gamma": {"heated_seats", "premium_audio", "sunroof"},
    }
    _MAX_EXTRAS = 3
    _DEFAULT_VERSION = 1

    def __init__(self) -> None:
        self._lock = RLock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._name: Optional[str] = None
            self._base: Optional[str] = None
            self._color: Optional[str] = None
            self._extras: List[str] = []
            self._version: Optional[int] = None

    def set_name(self, name: str) -> AssemblerInterface:
        with self._lock:
            self._name = name.strip()
            return self

    def choose_base(self, base: str) -> AssemblerInterface:
        with self._lock:
            self._base = base.strip().lower()
            return self

    def paint(self, color: str) -> AssemblerInterface:
        with self._lock:
            self._color = color.strip().lower()
            return self

    def add_extra(self, extra: str) -> AssemblerInterface:
        with self._lock:
            candidate = extra.strip().lower()
            if candidate and candidate not in self._extras:
                self._extras.append(candidate)
            return self

    def set_version(self, version: int) -> AssemblerInterface:
        with self._lock:
            if version is not None and version > 0:
                self._version = int(version)
            return self

    def _validate(self) -> None:
        if not self._base:
            raise ValueError("base component is required")
        if len(self._extras) > self._MAX_EXTRAS:
            raise ValueError(f"no more than {self._MAX_EXTRAS} extras allowed")
        allowed: Set[str] = self._COMPAT.get(self._base, set())
        invalid = [e for e in self._extras if e not in allowed]
        if invalid:
            raise ValueError(f"extras {invalid} incompatible with base '{self._base}'")

    def build(self) -> Product:
        with self._lock:
            self._validate()
            effective_version = self._version if self._version is not None else self._DEFAULT_VERSION
            name = self._name if self._name else f"{self._base}-{effective_version}"
            color = self._color if self._color else "standard"
            product = Product(
                name=name,
                base=self._base,
                color=color,
                extras=list(self._extras),
                version=effective_version,
            )
            # prepare for reuse
            self.reset()
            return product


class Coordinator:
    def __init__(self, assembler: AssemblerInterface) -> None:
        self._assembler = assembler

    def create_premium(self, base: str) -> Product:
        return (
            self._assembler
            .set_name(f"Premium-{base}")
            .choose_base(base)
            .paint("metallic")
            .add_extra("heated_seats")
            .add_extra("sunroof")
            .set_version(2)
            .build()
        )

    def create_basic(self, base: str) -> Product:
        return (
            self._assembler
            .choose_base(base)
            .paint("white")
            .set_version(1)
            .build()
        )


if __name__ == "__main__":
    assembler = StandardAssembler()
    director = Coordinator(assembler)

    p1 = director.create_premium("alpha")
    print(p1)

    p2 = director.create_basic("beta")
    print(p2)

    # direct fluent usage and reuse
    p3 = (
        assembler
        .choose_base("gamma")
        .paint("red")
        .add_extra("premium_audio")
        .add_extra("sunroof")
        .build()
    )
    print(p3)