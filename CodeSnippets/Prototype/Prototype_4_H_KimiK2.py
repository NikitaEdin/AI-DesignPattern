import copy
from typing import Any, Dict, List

class Registry:
    _templates: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, obj: Any) -> None:
        cls._templates[key] = obj

    @classmethod
    def retrieve(cls, key: str) -> Any:
        if key not in cls._templates:
            raise KeyError(f"Template '{key}' not found")
        return cls._templates[key]

class Address:
    def __init__(self, street: str, city: str) -> None:
        self.street = street
        self.city = city

    def clone(self, **overrides) -> 'Address':
        new = copy.deepcopy(self)
        for k, v in overrides.items():
            setattr(new, k, v)
        return new

class Employee:
    def __init__(self, name: str, age: int, address: Address, skills: List[str]) -> None:
        self.name = name
        self.age = age
        self.address = address
        self.skills = skills

    def clone(self, **overrides) -> 'Employee':
        new = copy.deepcopy(self)
        for k, v in overrides.items():
            if k == 'address' and isinstance(v, dict):
                new.address = self.address.clone(**v)
            else:
                setattr(new, k, v)
        return new

if __name__ == "__main__":
    hq_addr = Address("123 HQ St", "Metropolis")
    base = Employee("Alice", 30, hq_addr, ["Python", "Design"])

    Registry.register("base_employee", base)

    prototype = Registry.retrieve("base_employee")
    bob = prototype.clone(name="Bob", age=35, address={"street": "456 Branch Ave"})
    alice2 = prototype.clone(name="Alice II", skills=["Python", "Design", "Leadership"])

    print(vars(bob))
    print(vars(bob.address))
    print(vars(alice2))
    print(vars(alice2.address))