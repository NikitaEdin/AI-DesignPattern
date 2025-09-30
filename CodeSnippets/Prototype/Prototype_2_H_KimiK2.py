import copy
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import threading


class ReplicationError(Exception):
    pass


class Replicator(ABC):
    @abstractmethod
    def duplicate(self) -> Any:
        pass


class BlueprintManager:
    def __init__(self):
        self._registry: Dict[str, Replicator] = {}
        self._lock = threading.RLock()
    
    def register(self, name: str, instance: Replicator) -> None:
        with self._lock:
            if not isinstance(instance, Replicator):
                raise ReplicationError("Instance must implement Replicator")
            self._registry[name] = instance
    
    def unregister(self, name: str) -> None:
        with self._lock:
            self._registry.pop(name, None)
    
    def get_blueprint(self, name: str) -> Optional[Replicator]:
        with self._lock:
            if name not in self._registry:
                return None
            return copy.deepcopy(self._registry[name])


class ComplexObject(Replicator):
    def __init__(self, data: Dict[str, Any], metadata: Dict[str, Any]):
        self.data = copy.deepcopy(data)
        self.metadata = copy.deepcopy(metadata)
        self._creation_time = threading.current_thread().ident
    
    def duplicate(self) -> 'ComplexObject':
        try:
            return copy.deepcopy(self)
        except (TypeError, AttributeError) as e:
            raise ReplicationError(f"Failed to duplicate: {e}")
    
    def update_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComplexObject):
            return False
        return self.data == other.data and self.metadata == other.metadata


class ResourcePool:
    def __init__(self):
        self._manager = BlueprintManager()
        self._manager.register("default", ComplexObject({}, {}))
    
    def acquire(self, name: str = "default") -> ComplexObject:
        instance = self._manager.get_blueprint(name)
        if instance is None:
            raise ReplicationError(f"No such resource: {name}")
        return instance
    
    def register_pool(self, name: str, instance: ComplexObject) -> None:
        self._manager.register(name, instance)
    
    def dispose(self, name: str) -> None:
        self._manager.unregister(name)


def main():
    pool = ResourcePool()
    
    template = ComplexObject(
        data={"type": "processor", "cores": 8},
        metadata={"owner": "system", "priority": 10}
    )
    pool.register_pool("high-performance", template)
    
    instance1 = pool.acquire("high-performance")
    instance2 = pool.acquire("high-performance")
    
    instance1.update_metadata("priority", 5)
    print(instance1.metadata.get("priority") == 5)
    print(instance2.metadata.get("priority") == 10)
    print(instance1 is not instance2)


if __name__ == "__main__":
    main()