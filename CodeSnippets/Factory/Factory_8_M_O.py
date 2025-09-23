from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def operate(self) -> str:
        pass

class Printer(Device):
    def __init__(self, model: str, dpi: int = 300):
        super().__init__(model)
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        self.dpi = dpi

    def operate(self) -> str:
        return f"Printing from {self.model} at {self.dpi} DPI"

class Scanner(Device):
    def __init__(self, model: str, color: bool = True):
        super().__init__(model)
        self.color = bool(color)

    def operate(self) -> str:
        mode = "color" if self.color else "grayscale"
        return f"Scanning with {self.model} in {mode} mode"

class Fax(Device):
    def __init__(self, model: str, lines: int = 1):
        super().__init__(model)
        if lines < 1:
            raise ValueError("lines must be at least 1")
        self.lines = lines

    def operate(self) -> str:
        return f"Sending fax via {self.model} using {self.lines} line(s)"

class DeviceProducer:
    def __init__(self):
        self._registry = {}
        self._cache = {}

    def register(self, key: str, creator):
        if not callable(creator):
            raise TypeError("creator must be callable")
        self._registry[key] = creator

    def create(self, key: str, use_cache: bool = False, cache_key: str = None, **kwargs) -> Device:
        if key not in self._registry:
            raise ValueError(f"Unknown device type: {key}")
        effective_cache_key = cache_key or f"{key}:{sorted(kwargs.items())}"
        if use_cache and effective_cache_key in self._cache:
            return self._cache[effective_cache_key]
        device = self._registry[key](**kwargs)
        if not isinstance(device, Device):
            raise TypeError("creator must return a Device instance")
        if use_cache:
            self._cache[effective_cache_key] = device
        return device

if __name__ == "__main__":
    producer = DeviceProducer()
    producer.register("printer", lambda model, dpi=300: Printer(model, dpi))
    producer.register("scanner", lambda model, color=True: Scanner(model, color))
    producer.register("fax", lambda model, lines=1: Fax(model, lines))

    p1 = producer.create("printer", model="HP1000", dpi=600)
    s1 = producer.create("scanner", model="ScanPro", color=False)
    f1 = producer.create("fax", model="FaxMaster", lines=2)

    print(p1.operate())
    print(s1.operate())
    print(f1.operate())

    p_cached = producer.create("printer", use_cache=True, model="HP1000", dpi=600)
    p_cached2 = producer.create("printer", use_cache=True, model="HP1000", dpi=600)
    print("Cached same instance:", p_cached is p_cached2)

    try:
        producer.create("unknown", model="X")
    except ValueError as e:
        print("Error:", e)