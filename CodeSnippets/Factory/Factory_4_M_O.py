from abc import ABC, abstractmethod
from typing import Callable, Dict, Tuple, Any

class Service(ABC):
    @abstractmethod
    def perform(self) -> str:
        pass

class EmailService(Service):
    def __init__(self, recipient: str, message: str):
        if not recipient or not message:
            raise ValueError("recipient and message required")
        self.recipient = recipient
        self.message = message
    def perform(self) -> str:
        return f"Email to {self.recipient}: {self.message}"

class SmsService(Service):
    def __init__(self, phone_number: str, message: str):
        if not phone_number or not message:
            raise ValueError("phone_number and message required")
        self.phone_number = phone_number
        self.message = message
    def perform(self) -> str:
        return f"SMS to {self.phone_number}: {self.message}"

class PushService(Service):
    def __init__(self, device_id: str, message: str):
        if not device_id or not message:
            raise ValueError("device_id and message required")
        self.device_id = device_id
        self.message = message
    def perform(self) -> str:
        return f"Push to {self.device_id}: {self.message}"

class ServiceCreator:
    def __init__(self):
        self._registry: Dict[str, Callable[..., Service]] = {}
        self._cache: Dict[Tuple[str, Tuple[Tuple[str, Any], ...]], Service] = {}
    def register_service(self, key: str, constructor: Callable[..., Service]) -> None:
        if not callable(constructor):
            raise TypeError("constructor must be callable")
        self._registry[key] = constructor
    def create_service(self, key: str, use_cache: bool = False, **kwargs) -> Service:
        constructor = self._registry.get(key)
        if constructor is None:
            raise ValueError(f"Unknown service type: {key}")
        cache_key = (key, tuple(sorted(kwargs.items())))
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        try:
            instance = constructor(**kwargs)
        except TypeError as e:
            raise ValueError(f"Invalid parameters for {key}: {e}") from e
        if use_cache:
            self._cache[cache_key] = instance
        return instance

if __name__ == "__main__":
    creator = ServiceCreator()
    creator.register_service("email", EmailService)
    creator.register_service("sms", SmsService)
    creator.register_service("push", PushService)

    email = creator.create_service("email", recipient="alice@example.com", message="Hello Alice")
    print(email.perform())

    sms = creator.create_service("sms", phone_number="+123456789", message="Hi there")
    print(sms.perform())

    push = creator.create_service("push", device_id="device-42", message="You have a notification")
    print(push.perform())

    cached1 = creator.create_service("email", use_cache=True, recipient="bob@example.com", message="Cached")
    cached2 = creator.create_service("email", use_cache=True, recipient="bob@example.com", message="Cached")
    print(cached1 is cached2)

    try:
        creator.create_service("unknown", foo="bar")
    except ValueError as err:
        print("Error:", err)