from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json

class Product:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}
    
    def add_component(self, name: str, value: Any) -> None:
        self._components[name] = value
    
    def set_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value
    
    def get_component(self, name: str) -> Any:
        return self._components.get(name)
    
    def validate(self) -> bool:
        required = self._metadata.get('required_components', [])
        return all(comp in self._components for comp in required)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'components': self._components.copy(),
            'metadata': self._metadata.copy()
        }

class AbstractConstructor(ABC):
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        self._product = Product()
    
    @property
    def product(self) -> Product:
        result = self._product
        self.reset()
        return result
    
    @abstractmethod
    def configure_base(self, **kwargs) -> 'AbstractConstructor':
        pass
    
    @abstractmethod
    def add_features(self, features: List[str]) -> 'AbstractConstructor':
        pass

class WebAppConstructor(AbstractConstructor):
    def configure_base(self, framework: str = "flask", port: int = 8080) -> 'AbstractConstructor':
        self._product.add_component("framework", framework)
        self._product.add_component("port", port)
        self._product.set_metadata("type", "web_application")
        self._product.set_metadata("required_components", ["framework", "routes"])
        return self
    
    def add_features(self, features: List[str]) -> 'AbstractConstructor':
        feature_config = {}
        for feature in features:
            if feature == "database":
                feature_config["database"] = {"type": "postgresql", "pool_size": 10}
            elif feature == "auth":
                feature_config["authentication"] = {"method": "jwt", "expiry": 3600}
            elif feature == "cache":
                feature_config["caching"] = {"backend": "redis", "ttl": 300}
        
        self._product.add_component("features", feature_config)
        return self
    
    def set_routes(self, routes: Dict[str, str]) -> 'AbstractConstructor':
        self._product.add_component("routes", routes)
        return self
    
    def configure_security(self, ssl: bool = True, cors: bool = True) -> 'AbstractConstructor':
        security_config = {"ssl_enabled": ssl, "cors_enabled": cors}
        self._product.add_component("security", security_config)
        return self

class Director:
    def __init__(self, constructor: AbstractConstructor):
        self._constructor = constructor
    
    def create_basic_app(self) -> Product:
        return (self._constructor
                .configure_base(framework="flask", port=5000)
                .set_routes({"/": "home", "/api": "api_handler"})
                .add_features(["database"])
                .product)
    
    def create_enterprise_app(self) -> Product:
        return (self._constructor
                .configure_base(framework="django", port=8080)
                .set_routes({"/": "home", "/api": "api_handler", "/admin": "admin_panel"})
                .add_features(["database", "auth", "cache"])
                .configure_security(ssl=True, cors=True)
                .product)
    
    def create_from_config(self, config: Dict[str, Any]) -> Optional[Product]:
        try:
            constructor = self._constructor.configure_base(**config.get("base", {}))
            
            if "routes" in config:
                constructor = constructor.set_routes(config["routes"])
            
            if "features" in config:
                constructor = constructor.add_features(config["features"])
            
            if "security" in config:
                constructor = constructor.configure_security(**config["security"])
            
            product = constructor.product
            return product if product.validate() else None
        except Exception:
            return None

if __name__ == "__main__":
    constructor = WebAppConstructor()
    director = Director(constructor)
    
    basic_app = director.create_basic_app()
    print("Basic App:", json.dumps(basic_app.to_dict(), indent=2))
    print("Valid:", basic_app.validate())
    
    enterprise_app = director.create_enterprise_app()
    print("\nEnterprise App:", json.dumps(enterprise_app.to_dict(), indent=2))
    print("Valid:", enterprise_app.validate())
    
    custom_config = {
        "base": {"framework": "fastapi", "port": 3000},
        "routes": {"/health": "health_check", "/metrics": "metrics"},
        "features": ["cache", "auth"],
        "security": {"ssl": True, "cors": False}
    }
    
    custom_app = director.create_from_config(custom_config)
    if custom_app:
        print("\nCustom App:", json.dumps(custom_app.to_dict(), indent=2))
        print("Valid:", custom_app.validate())