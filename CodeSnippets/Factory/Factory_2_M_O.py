import abc
from typing import Dict, Type, Any

class Peripheral(abc.ABC):
    def __init__(self, name: str):
        self.name = name
    @abc.abstractmethod
    def operate(self, payload: Any) -> str:
        ...

class Printer(Peripheral):
    def operate(self, payload: Any) -> str:
        return f"Printer '{self.name}' printed: {payload}"

class Scanner(Peripheral):
    def operate(self, payload: Any) -> str:
        return f"Scanner '{self.name}' scanned: {payload}"

class Camera(Peripheral):
    def operate(self, payload: Any) -> str:
        return f"Camera '{self.name}' captured: {payload}"

class DeviceCreator:
    def __init__(self):
        self._registry: Dict[str, Type[Peripheral]] = {}
        self._singletons: Dict[str, Peripheral] = {}
    def register_device_type(self, key: str, cls: Type[Peripheral]):
        if not isinstance(key, str) or not issubclass(cls, Peripheral):
            raise TypeError("Invalid registration: key must be str and cls a Peripheral subclass")
        self._registry[key] = cls
    def create_device(self, key: str, name: str, singleton: bool = False, **kwargs) -> Peripheral:
        if key not in self._registry:
            raise ValueError(f"Unknown device type: {key}")
        if singleton and key in self._singletons:
            return self._singletons[key]
        cls = self._registry[key]
        instance = cls(name, **kwargs)
        if singleton:
            self._singletons[key] = instance
        return instance

if __name__ == "__main__":
    maker = DeviceCreator()
    maker.register_device_type("printer", Printer)
    maker.register_device_type("scanner", Scanner)
    maker.register_device_type("camera", Camera)

    p1 = maker.create_device("printer", "HP-101")
    s1 = maker.create_device("scanner", "ScanPro")
    c1 = maker.create_device("camera", "CamX", singleton=True)
    c2 = maker.create_device("camera", "OtherName", singleton=True)

    print(p1.operate("Document A"))
    print(s1.operate("Page 1"))
    print(c1.operate("Photo1"))
    print("Same camera instance:", c1 is c2)

    try:
        maker.create_device("unknown", "Nope")
    except ValueError as e:
        print("Error:", e)