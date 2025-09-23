from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json

class Product:
    def __init__(self):
        self._components: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}
    
    def add_component(self, name: str, value: Any) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Component name must be a non-empty string")
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
        self._product = Product()
    
    @abstractmethod
    def add_core_features(self) -> 'AbstractConstructor':
        pass
    
    @abstractmethod
    def add_optional_features(self) -> 'AbstractConstructor':
        pass
    
    def reset(self) -> 'AbstractConstructor':
        self._product = Product()
        return self
    
    def finalize(self) -> Product:
        if not self._product.validate():
            missing = [c for c in self._product._metadata.get('required_components', []) 
                      if c not in self._product._components]
            raise RuntimeError(f"Invalid product: missing components {missing}")
        return self._product

class WebsiteConstructor(AbstractConstructor):
    def __init__(self):
        super().__init__()
        self._product.set_metadata('required_components', ['layout', 'content'])
        self._product.set_metadata('type', 'website')
    
    def add_core_features(self) -> 'WebsiteConstructor':
        self._product.add_component('layout', 'responsive')
        self._product.add_component('content', 'default_content')
        return self
    
    def add_optional_features(self) -> 'WebsiteConstructor':
        self._product.add_component('analytics', 'google_analytics')
        self._product.add_component('seo', 'meta_tags')
        return self
    
    def set_theme(self, theme: str) -> 'WebsiteConstructor':
        self._product.add_component('theme', theme)
        return self
    
    def add_database(self, db_type: str) -> 'WebsiteConstructor':
        self._product.add_component('database', db_type)
        return self

class APIConstructor(AbstractConstructor):
    def __init__(self):
        super().__init__()
        self._product.set_metadata('required_components', ['endpoints', 'authentication'])
        self._product.set_metadata('type', 'api')
    
    def add_core_features(self) -> 'APIConstructor':
        self._product.add_component('endpoints', ['/health', '/status'])
        self._product.add_component('authentication', 'jwt')
        return self
    
    def add_optional_features(self) -> 'APIConstructor':
        self._product.add_component('rate_limiting', 'token_bucket')
        self._product.add_component('documentation', 'swagger')
        return self
    
    def set_version(self, version: str) -> 'APIConstructor':
        self._product.add_component('version', version)
        return self

class Director:
    @staticmethod
    def create_basic_website(constructor: WebsiteConstructor) -> Product:
        return constructor.reset().add_core_features().finalize()
    
    @staticmethod
    def create_premium_website(constructor: WebsiteConstructor) -> Product:
        return (constructor.reset()
                .add_core_features()
                .add_optional_features()
                .set_theme('premium')
                .add_database('postgresql')
                .finalize())
    
    @staticmethod
    def create_rest_api(constructor: APIConstructor) -> Product:
        return (constructor.reset()
                .add_core_features()
                .add_optional_features()
                .set_version('v1')
                .finalize())

if __name__ == "__main__":
    website_constructor = WebsiteConstructor()
    api_constructor = APIConstructor()
    
    basic_site = Director.create_basic_website(website_constructor)
    premium_site = Director.create_premium_website(website_constructor)
    api = Director.create_rest_api(api_constructor)
    
    custom_site = (website_constructor.reset()
                   .add_core_features()
                   .set_theme('dark')
                   .finalize())
    
    print("Basic Website:", json.dumps(basic_site.to_dict(), indent=2))
    print("\nPremium Website:", json.dumps(premium_site.to_dict(), indent=2))
    print("\nREST API:", json.dumps(api.to_dict(), indent=2))
    print("\nCustom Website:", json.dumps(custom_site.to_dict(), indent=2))