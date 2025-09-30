import functools
from typing import Optional, Dict, Any

class ServerSpec:
    __slots__ = ("cpu", "ram_gb", "disk_gb", "gpu", "extras")

    def __init__(self):
        self.cpu: Optional[int] = None
        self.ram_gb: Optional[int] = None
        self.disk_gb: Optional[int] = None
        self.gpu: Optional[str] = None
        self.extras: Dict[str, Any] = {}

    def __repr__(self) -> str:
        return (f"ServerSpec(cpu={self.cpu}, ram_gb={self.ram_gb}, "
                f"disk_gb={self.disk_gb}, gpu={self.gpu}, extras={self.extras})")

class ServerConfigurator:
    def __init__(self):
        self._spec = ServerSpec()

    def with_cpu(self, cores: int) -> "ServerConfigurator":
        if cores <= 0:
            raise ValueError("CPU cores must be positive")
        self._spec.cpu = cores
        return self

    def with_ram(self, gb: int) -> "ServerConfigurator":
        if gb <= 0:
            raise ValueError("RAM must be positive")
        self._spec.ram_gb = gb
        return self

    def with_disk(self, gb: int) -> "ServerConfigurator":
        if gb <= 0:
            raise ValueError("Disk must be positive")
        self._spec.disk_gb = gb
        return self

    def with_gpu(self, model: str) -> "ServerConfigurator":
        self._spec.gpu = model
        return self

    def add_extra(self, key: str, value: Any) -> "ServerConfigurator":
        self._spec.extras[key] = value
        return self

    def validate(self) -> None:
        if None in (self._spec.cpu, self._spec.ram_gb, self._spec.disk_gb):
            raise RuntimeError("Missing required fields: cpu, ram_gb, disk_gb")

    def finalize(self) -> ServerSpec:
        self.validate()
        return self._spec

    def reset(self) -> "ServerConfigurator":
        self._spec = ServerSpec()
        return self

if __name__ == "__main__":
    cfg = ServerConfigurator()
    cfg.with_cpu(16).with_ram(64).with_disk(512).with_gpu("A100")
    cfg.add_extra("region", "us-west-2").add_extra("spot", True)
    server = cfg.finalize()
    print(server)

    cfg.reset()
    server2 = cfg.with_cpu(8).with_ram(32).with_disk(256).finalize()
    print(server2)