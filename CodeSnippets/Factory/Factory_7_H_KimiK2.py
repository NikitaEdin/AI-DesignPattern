from __future__ import annotations
import abc
import random
import string
import threading
import weakref
from typing import Dict, Type, Optional, Set

class CloudService(abc.ABC):
    @abc.abstractmethod
    def deploy(self, name: str) -> str: ...

class AWSService(CloudService):
    def deploy(self, name: str) -> str:
        return f"[AWS] EC2 instance '{name}' running on us-east-1"

class GCPService(CloudService):
    def deploy(self, name: str) -> str:
        return f"[GCP] Compute VM '{name}' in us-central1"

class AzureService(CloudService):
    def deploy(self, name: str) -> str:
        return f"[Azure] Virtual Machine '{name}' in East US"

class ServiceProvider:
    _registry: Dict[str, Type[CloudService]] = {}
    _lock = threading.Lock()
    _instances: Dict[str, weakref.ref] = {}

    @classmethod
    def register(cls, key: str, service_cls: Type[CloudService]) -> None:
        with cls._lock:
            cls._registry[key.lower()] = service_cls

    @classmethod
    def create(cls, key: str, **kwargs) -> CloudService:
        key = key.lower()
        with cls._lock:
            if key not in cls._registry:
                raise ValueError(f"Unknown service '{key}'")
            if key in cls._instances:
                existing = cls._instances[key]()
                if existing:
                    return existing
            service = cls._registry[key](**kwargs)
            cls._instances[key] = weakref.ref(service)
            return service

    @classmethod
    def list_services(cls) -> Set[str]:
        return set(cls._registry.keys())

def generate_name(prefix: str = "app") -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}-{suffix}"

if __name__ == "__main__":
    ServiceProvider.register("aws", AWSService)
    ServiceProvider.register("gcp", GCPService)
    ServiceProvider.register("azure", AzureService)

    for provider in ("aws", "gcp", "azure", "aws"):
        svc = ServiceProvider.create(provider)
        print(svc.deploy(generate_name()))

    print("Available:", ServiceProvider.list_services())