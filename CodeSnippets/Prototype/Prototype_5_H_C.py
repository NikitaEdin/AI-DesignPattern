import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union

class Cloneable(ABC):
    @abstractmethod
    def clone(self) -> 'Cloneable':
        pass
    
    @abstractmethod
    def get_id(self) -> str:
        pass

class Document(Cloneable):
    def __init__(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        self._title = title
        self._content = content
        self._metadata = metadata or {}
        self._version = 1
        self._parent_id = None
        
    def clone(self) -> 'Document':
        cloned = Document(self._title, self._content, copy.deepcopy(self._metadata))
        cloned._version = self._version + 1
        cloned._parent_id = self.get_id()
        return cloned
    
    def get_id(self) -> str:
        return f"{self._title}_{id(self)}"
    
    def update_content(self, content: str) -> None:
        self._content = content
    
    def add_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value
    
    def __str__(self) -> str:
        parent_info = f" (derived from {self._parent_id})" if self._parent_id else ""
        return f"Document: {self._title} v{self._version}{parent_info}"

class Blueprint(Cloneable):
    def __init__(self, name: str, components: Optional[Dict[str, Union[str, int, float]]] = None):
        self._name = name
        self._components = components or {}
        self._complexity_score = self._calculate_complexity()
        
    def clone(self) -> 'Blueprint':
        cloned_components = copy.deepcopy(self._components)
        cloned = Blueprint(f"Copy_of_{self._name}", cloned_components)
        return cloned
    
    def get_id(self) -> str:
        return f"blueprint_{self._name}_{hash(frozenset(self._components.items()))}"
    
    def add_component(self, name: str, spec: Union[str, int, float]) -> None:
        self._components[name] = spec
        self._complexity_score = self._calculate_complexity()
    
    def _calculate_complexity(self) -> int:
        return len(self._components) + sum(1 for v in self._components.values() if isinstance(v, str) and len(v) > 10)
    
    def __str__(self) -> str:
        return f"Blueprint: {self._name} (Complexity: {self._complexity_score}, Components: {len(self._components)})"

class CloneRegistry:
    def __init__(self):
        self._registry: Dict[str, Cloneable] = {}
    
    def register(self, key: str, template: Cloneable) -> None:
        self._registry[key] = template
    
    def create(self, key: str) -> Optional[Cloneable]:
        template = self._registry.get(key)
        return template.clone() if template else None
    
    def list_templates(self) -> Dict[str, str]:
        return {key: str(template) for key, template in self._registry.items()}

if __name__ == "__main__":
    registry = CloneRegistry()
    
    base_doc = Document("Project Spec", "Initial requirements document", 
                       {"author": "Alice", "department": "Engineering"})
    complex_blueprint = Blueprint("Server_Config", {
        "cpu_cores": 8,
        "memory": "32GB",
        "storage": "high_performance_ssd_with_encryption",
        "network": "10Gbps_ethernet_bonded_interface"
    })
    
    registry.register("standard_doc", base_doc)
    registry.register("server_template", complex_blueprint)
    
    print("=== Registry Templates ===")
    for key, desc in registry.list_templates().items():
        print(f"{key}: {desc}")
    
    print("\n=== Creating Clones ===")
    doc_clone1 = registry.create("standard_doc")
    doc_clone2 = registry.create("standard_doc")
    blueprint_clone = registry.create("server_template")
    
    if doc_clone1:
        doc_clone1.update_content("Modified requirements for mobile app")
        doc_clone1.add_metadata("modified_by", "Bob")
    
    if doc_clone2:
        doc_clone2.update_content("Requirements for web platform")
        doc_clone2.add_metadata("priority", "high")
    
    if blueprint_clone:
        blueprint_clone.add_component("backup_storage", "redundant_raid_array")
    
    print(f"Original: {base_doc}")
    print(f"Clone 1: {doc_clone1}")
    print(f"Clone 2: {doc_clone2}")
    print(f"Original Blueprint: {complex_blueprint}")
    print(f"Blueprint Clone: {blueprint_clone}")