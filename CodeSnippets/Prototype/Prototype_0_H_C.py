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

class CloneRegistry:
    _instance = None
    _registry: Dict[str, Cloneable] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, key: str, obj: Cloneable) -> None:
        self._registry[key] = obj
    
    def get_clone(self, key: str) -> Optional[Cloneable]:
        if key in self._registry:
            return self._registry[key].clone()
        return None
    
    def get_deep_clone(self, key: str) -> Optional[Cloneable]:
        if key in self._registry:
            return self._registry[key].deep_clone()
        return None

class Document(Cloneable):
    def __init__(self, title: str, content: str, metadata: Dict[str, Any] = None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.version = 1
        self._id = id(self)
    
    def clone(self) -> 'Document':
        new_doc = Document(self.title, self.content, self.metadata.copy())
        new_doc.version = self.version
        return new_doc
    
    def deep_clone(self) -> 'Document':
        new_doc = Document(
            self.title,
            self.content,
            copy.deepcopy(self.metadata)
        )
        new_doc.version = self.version + 1
        return new_doc
    
    def update_content(self, new_content: str) -> None:
        self.content = new_content
        self.version += 1
    
    def __str__(self) -> str:
        return f"Document(id={self._id}, title='{self.title}', version={self.version})"

class ConfigTemplate(Cloneable):
    def __init__(self, name: str, settings: Dict[str, Any]):
        self.name = name
        self.settings = settings
        self.created_instances = 0
    
    def clone(self) -> 'ConfigTemplate':
        cloned = ConfigTemplate(self.name, self.settings.copy())
        self.created_instances += 1
        cloned.name = f"{self.name}_copy_{self.created_instances}"
        return cloned
    
    def deep_clone(self) -> 'ConfigTemplate':
        cloned = ConfigTemplate(self.name, copy.deepcopy(self.settings))
        self.created_instances += 1
        cloned.name = f"{self.name}_deep_copy_{self.created_instances}"
        return cloned
    
    def get_setting(self, key: str) -> Any:
        return self.settings.get(key)
    
    def update_setting(self, key: str, value: Any) -> None:
        self.settings[key] = value

if __name__ == "__main__":
    registry = CloneRegistry()
    
    base_doc = Document("Template", "Initial content", {"author": "System", "tags": ["template"]})
    config = ConfigTemplate("base_config", {"debug": True, "timeout": 30, "features": ["auth", "logging"]})
    
    registry.register("document_template", base_doc)
    registry.register("base_config", config)
    
    doc1 = registry.get_clone("document_template")
    doc1.title = "User Guide"
    doc1.update_content("User guide content")
    
    doc2 = registry.get_deep_clone("document_template")
    doc2.title = "API Documentation"
    doc2.metadata["tags"].append("api")
    
    config1 = registry.get_clone("base_config")
    config1.update_setting("debug", False)
    
    config2 = registry.get_deep_clone("base_config")
    config2.settings["features"].append("metrics")
    
    print(f"Original: {base_doc}")
    print(f"Clone 1: {doc1}")
    print(f"Clone 2: {doc2}")
    print(f"Original tags: {base_doc.metadata['tags']}")
    print(f"Clone 2 tags: {doc2.metadata['tags']}")
    
    print(f"\nOriginal config features: {config.get_setting('features')}")
    print(f"Deep cloned config features: {config2.get_setting('features')}")