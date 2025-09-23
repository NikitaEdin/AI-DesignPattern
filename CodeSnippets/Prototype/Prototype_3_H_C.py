from abc import ABC, abstractmethod
import copy
from typing import Dict, Any, Optional
from datetime import datetime

class Cloneable(ABC):
    def __init__(self):
        self._creation_time = datetime.now()
        self._clone_count = 0
    
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    def get_clone_info(self) -> Dict[str, Any]:
        return {
            'original_creation': self._creation_time,
            'clone_count': self._clone_count
        }

class Document(Cloneable):
    def __init__(self, title: str = "", content: str = "", metadata: Optional[Dict] = None):
        super().__init__()
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self._revisions = []
    
    def clone(self) -> 'Document':
        cloned = copy.deepcopy(self)
        cloned._creation_time = datetime.now()
        cloned._clone_count = 0
        self._clone_count += 1
        cloned._revisions = []
        return cloned
    
    def add_revision(self, change: str):
        self._revisions.append({
            'timestamp': datetime.now(),
            'change': change
        })
    
    def __str__(self):
        return f"Document(title='{self.title}', revisions={len(self._revisions)})"

class Configuration(Cloneable):
    def __init__(self, name: str = "", settings: Optional[Dict] = None):
        super().__init__()
        self.name = name
        self._settings = settings or {}
        self._locked = False
    
    def clone(self) -> 'Configuration':
        if self._locked:
            raise RuntimeError("Cannot clone locked configuration")
        
        cloned = copy.deepcopy(self)
        cloned._creation_time = datetime.now()
        cloned._clone_count = 0
        cloned._locked = False
        self._clone_count += 1
        return cloned
    
    def set_setting(self, key: str, value: Any):
        if not self._locked:
            self._settings[key] = value
    
    def lock(self):
        self._locked = True
    
    def get_setting(self, key: str, default=None):
        return self._settings.get(key, default)

class Registry:
    def __init__(self):
        self._templates: Dict[str, Cloneable] = {}
    
    def register(self, name: str, template: Cloneable):
        self._templates[name] = template
    
    def create(self, name: str) -> Optional[Cloneable]:
        template = self._templates.get(name)
        if template:
            return template.clone()
        return None
    
    def list_templates(self) -> list:
        return list(self._templates.keys())

if __name__ == "__main__":
    registry = Registry()
    
    base_doc = Document("Template Doc", "Base content", {"author": "System"})
    base_config = Configuration("Default Config", {"debug": True, "port": 8080})
    
    registry.register("document_template", base_doc)
    registry.register("server_config", base_config)
    
    doc1 = registry.create("document_template")
    doc1.title = "Report #1"
    doc1.add_revision("Updated title")
    
    doc2 = registry.create("document_template")
    doc2.title = "Report #2"
    doc2.content = "Different content"
    
    config1 = registry.create("server_config")
    config1.set_setting("port", 9000)
    config1.lock()
    
    try:
        locked_clone = config1.clone()
    except RuntimeError as e:
        print(f"Expected error: {e}")
    
    print(f"Created documents: {doc1}, {doc2}")
    print(f"Base document clone count: {base_doc.get_clone_info()['clone_count']}")
    print(f"Available templates: {registry.list_templates()}")
    print(f"Config1 port: {config1.get_setting('port')}")