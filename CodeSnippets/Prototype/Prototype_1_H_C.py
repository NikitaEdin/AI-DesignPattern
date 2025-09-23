import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Cloneable(ABC):
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    @abstractmethod
    def deep_clone(self) -> 'Cloneable':
        pass

class Configuration(Cloneable):
    def __init__(self, name: str, settings: Dict[str, Any], metadata: Optional[Dict] = None):
        self.name = name
        self.settings = settings
        self.metadata = metadata or {}
        self._version = 1
        
    def clone(self) -> 'Configuration':
        return Configuration(
            self.name,
            self.settings.copy(),
            self.metadata.copy()
        )
    
    def deep_clone(self) -> 'Configuration':
        cloned = Configuration(
            self.name,
            copy.deepcopy(self.settings),
            copy.deepcopy(self.metadata)
        )
        cloned._version = self._version
        return cloned
    
    def update_setting(self, key: str, value: Any):
        self.settings[key] = value
        self._version += 1
    
    def serialize(self) -> str:
        return json.dumps({
            'name': self.name,
            'settings': self.settings,
            'metadata': self.metadata,
            'version': self._version
        })
    
    @classmethod
    def deserialize(cls, data: str) -> 'Configuration':
        obj_data = json.loads(data)
        instance = cls(obj_data['name'], obj_data['settings'], obj_data['metadata'])
        instance._version = obj_data['version']
        return instance

class ConfigurationRegistry:
    def __init__(self):
        self._templates: Dict[str, Configuration] = {}
        self._cache: Dict[str, Configuration] = {}
    
    def register(self, key: str, template: Configuration):
        self._templates[key] = template.deep_clone()
    
    def create(self, key: str, deep: bool = False) -> Optional[Configuration]:
        if key not in self._templates:
            return None
        
        cache_key = f"{key}_{'deep' if deep else 'shallow'}"
        if cache_key not in self._cache:
            template = self._templates[key]
            self._cache[cache_key] = template.deep_clone() if deep else template.clone()
        
        return self._cache[cache_key].deep_clone() if deep else self._cache[cache_key].clone()
    
    def clear_cache(self):
        self._cache.clear()

if __name__ == "__main__":
    registry = ConfigurationRegistry()
    
    base_config = Configuration(
        "database_config",
        {
            "host": "localhost",
            "port": 5432,
            "connection_pool": {"min": 5, "max": 20}
        },
        {"created_by": "system", "environment": "production"}
    )
    
    registry.register("db_template", base_config)
    
    config1 = registry.create("db_template", deep=True)
    config2 = registry.create("db_template", deep=False)
    
    config1.update_setting("host", "production-server")
    config1.settings["connection_pool"]["max"] = 50
    
    config2.update_setting("port", 3306)
    
    print(f"Original: {base_config.settings}")
    print(f"Config1: {config1.settings}")
    print(f"Config2: {config2.settings}")
    
    serialized = config1.serialize()
    restored_config = Configuration.deserialize(serialized)
    print(f"Restored: {restored_config.settings}")