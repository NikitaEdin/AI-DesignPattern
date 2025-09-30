import threading
from typing import Any, Dict, Optional

class ApplicationHub:
    _instance: Optional['ApplicationHub'] = None
    _lock = threading.Lock()
    
    def __new__(cls, config: Optional[Dict[str, Any]] = None) -> 'ApplicationHub':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._config = config or {}
                    cls._instance._services = {}
                    cls._instance._initialized = True
        return cls._instance
    
    def register_service(self, name: str, service: Any) -> None:
        self._services[name] = service
    
    def get_service(self, name: str) -> Any:
        return self._services.get(name)
    
    def get_config(self) -> Dict[str, Any]:
        return self._config.copy()
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        self._config.update(updates)
    
    def clear_services(self) -> None:
        self._services.clear()

if __name__ == "__main__":
    hub1 = ApplicationHub({'debug': True, 'port': 8080})
    hub2 = ApplicationHub({'debug': False, 'port': 9090})
    
    print(hub1 is hub2)
    print(hub1.get_config())
    
    hub1.register_service('database', 'PostgreSQL')
    print(hub2.get_service('database'))
    
    hub2.update_config({'host': 'localhost'})
    print(hub1.get_config())
    
    hub1.clear_services()
    print(hub2.get_service('database'))