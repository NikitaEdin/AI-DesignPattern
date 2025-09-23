import copy
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any


class Clonable(ABC):
    @abstractmethod
    def clone(self, deep: bool = True):
        pass


@dataclass
class DocumentTemplate(Clonable):
    identifier: str
    title: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def clone(self, deep: bool = True):
        if deep:
            cloned = copy.deepcopy(self)
            cloned.identifier = str(uuid.uuid4())
            return cloned
        else:
            cloned = copy.copy(self)
            cloned.identifier = str(uuid.uuid4())
            return cloned


class TemplateRegistry:
    def __init__(self):
        self._store: Dict[str, Clonable] = {}

    def register(self, key: str, template: Clonable):
        if not isinstance(template, Clonable):
            raise TypeError("Only clonable objects can be registered")
        self._store[key] = template

    def unregister(self, key: str):
        if key not in self._store:
            raise KeyError(f"No template registered under key: {key}")
        del self._store[key]

    def create_copy(self, key: str, deep: bool = True) -> Clonable:
        if key not in self._store:
            raise KeyError(f"No template registered under key: {key}")
        return self._store[key].clone(deep=deep)


if __name__ == "__main__":
    registry = TemplateRegistry()
    base_report = DocumentTemplate(
        identifier=str(uuid.uuid4()),
        title="Quarterly Report",
        content="Confidential financials",
        metadata={"author": "Alice", "tags": ["finance", "Q1"]}
    )
    base_invoice = DocumentTemplate(
        identifier=str(uuid.uuid4()),
        title="Invoice",
        content="Billing details",
        metadata={"company": "Acme", "terms": {"net": 30}}
    )

    registry.register("report", base_report)
    registry.register("invoice", base_invoice)

    shallow_copy = registry.create_copy("report", deep=False)
    deep_copy = registry.create_copy("invoice", deep=True)

    shallow_copy.metadata["tags"].append("draft")
    deep_copy.metadata["terms"]["net"] = 45

    print("Original report metadata:", base_report.metadata)
    print("Shallow copy metadata:", shallow_copy.metadata)
    print("Original invoice metadata:", base_invoice.metadata)
    print("Deep copy metadata:", deep_copy.metadata)
    print("Original report id:", base_report.identifier)
    print("Shallow copy id:", shallow_copy.identifier)
    print("Original invoice id:", base_invoice.identifier)
    print("Deep copy id:", deep_copy.identifier)