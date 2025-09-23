import abc
from typing import Callable, Dict, Type
from dataclasses import dataclass

class UnknownReportError(Exception):
    pass

class ReportBase(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> str:
        pass

@dataclass
class SummaryReport(ReportBase):
    title: str
    overview: str

    def generate(self) -> str:
        return f"Summary: {self.title}\n{self.overview[:120]}"

@dataclass
class DetailedReport(ReportBase):
    title: str
    content: str
    author: str

    def generate(self) -> str:
        header = f"Detailed Report - {self.title} by {self.author}"
        return f"{header}\n{self.content}"

class ReportCreator:
    def __init__(self) -> None:
        self._registry: Dict[str, Callable[..., ReportBase]] = {}
        self._cache: Dict[str, ReportBase] = {}

    def register(self, key: str, constructor: Callable[..., ReportBase], overwrite: bool = False) -> None:
        if key in self._registry and not overwrite:
            raise ValueError(f"Key '{key}' already registered")
        self._registry[key] = constructor

    def create(self, key: str, use_cache: bool = True, **kwargs) -> ReportBase:
        if use_cache and key in self._cache:
            return self._cache[key]
        constructor = self._registry.get(key)
        if not constructor:
            raise UnknownReportError(f"No constructor for type '{key}'")
        try:
            instance = constructor(**kwargs)
        except TypeError as exc:
            raise ValueError(f"Invalid parameters for '{key}': {exc}") from exc
        if use_cache:
            self._cache[key] = instance
        return instance

if __name__ == "__main__":
    creator = ReportCreator()
    creator.register("summary", lambda title, overview: SummaryReport(title=title, overview=overview))
    creator.register("detailed", lambda title, content, author="Unknown": DetailedReport(title=title, content=content, author=author))

    s1 = creator.create("summary", title="Q1 Results", overview="Performance improved across all metrics.")
    d1 = creator.create("detailed", title="Q1 Deep Dive", content="Lots of detailed analysis...", author="Analyst A")
    s2 = creator.create("summary")  # will raise due to missing kwargs if not cached
    print(s1.generate())
    print(d1.generate())
    print("Cached summary is same instance:", s1 is s2)