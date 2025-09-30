import copy
from typing import Dict, Any, Optional


class Replicable:
    __slots__ = ()

    def duplicate(self, deep: bool = True, **overrides) -> 'Replicable':
        new = copy.deepcopy(self) if deep else copy.copy(self)
        for k, v in overrides.items():
            if not hasattr(new, k):
                raise AttributeError(f"Invalid attribute: {k}")
            setattr(new, k, v)
        return new


class Component(Replicable):
    __slots__ = ("_identity", "_meta")

    def __init__(self, identity: str, **meta) -> None:
        self._identity = identity
        self._meta: Dict[str, Any] = meta

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._identity})"


class Registry:
    __slots__ = ("_blueprints",)

    def __init__(self) -> None:
        self._blueprints: Dict[str, Replicable] = {}

    def register(self, key: str, item: Replicable) -> None:
        self._blueprints[key] = item

    def create(self, key: str, **overrides) -> Replicable:
        try:
            return self._blueprints[key].duplicate(**overrides)
        except KeyError:
            raise KeyError(f"No blueprint for key {key}")


class Scene:
    __slots__ = ("_registry", "_cache")

    def __init__(self) -> None:
        self._registry = Registry()
        self._cache: Dict[str, Replicable] = {}

    def add_blueprint(self, key: str, item: Replicable) -> None:
        self._registry.register(key, item)

    def spawn(self, key: str, cache_key: Optional[str] = None, **overrides) -> Replicable:
        obj = self._registry.create(key, **overrides)
        if cache_key:
            self._cache[cache_key] = obj
        return obj

    def retrieve(self, cache_key: str) -> Replicable:
        return self._cache[cache_key].duplicate()


def main():
    scene = Scene()
    archer = Component("Archer", health=100, damage=15)
    knight = Component("Knight", health=150, damage=20)

    scene.add_blueprint("archer", archer)
    scene.add_blueprint("knight", knight)

    a1 = scene.spawn("archer", cache_key="archer_1", damage=18)
    k1 = scene.spawn("knight")
    a2 = scene.spawn("archer", health=90)

    a3 = scene.retrieve("archer_1")

    print(a1, a2, a3, k1)


if __name__ == "__main__":
    main()