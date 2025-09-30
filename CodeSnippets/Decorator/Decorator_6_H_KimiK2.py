from abc import ABC, abstractmethod
from functools import wraps
import time

class DataSource(ABC):
    @abstractmethod
    def read(self) -> str:
        pass
    
    @abstractmethod
    def write(self, data: str) -> None:
        pass

class FileStorage(DataSource):
    def __init__(self, filename: str):
        self.filename = filename
    
    def read(self) -> str:
        try:
            with open(self.filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def write(self, data: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(data)

class DataEnhancer(DataSource):
    def __init__(self, source: DataSource):
        self._source = source
    
    def read(self) -> str:
        return self._source.read()
    
    def write(self, data: str) -> None:
        self._source.write(data)

class CompressionWrapper(DataEnhancer):
    def read(self) -> str:
        data = super().read()
        return self._decompress(data)
    
    def write(self, data: str) -> None:
        compressed = self._compress(data)
        super().write(compressed)
    
    def _compress(self, data: str) -> str:
        return f"[COMPRESSED:{len(data)}|{data}]"
    
    def _decompress(self, data: str) -> str:
        if data.startswith("[COMPRESSED:"):
            return data.split("|", 1)[1][:-1]
        return data

class EncryptionWrapper(DataEnhancer):
    def __init__(self, source: DataSource, key: str = "default_key"):
        super().__init__(source)
        self.key = key
    
    def read(self) -> str:
        data = super().read()
        return self._decrypt(data)
    
    def write(self, data: str) -> None:
        encrypted = self._encrypt(data)
        super().write(encrypted)
    
    def _encrypt(self, data: str) -> str:
        encrypted = ''.join(chr(ord(c) + len(self.key)) for c in data)
        return f"[ENCRYPTED|{encrypted}]"
    
    def _decrypt(self, data: str) -> str:
        if data.startswith("[ENCRYPTED|"):
            encrypted = data[11:-1]
            return ''.join(chr(ord(c) - len(self.key)) for c in encrypted)
        return data

class LoggingWrapper(DataEnhancer):
    def read(self) -> str:
        start = time.time()
        data = super().read()
        print(f"[LOG] Read {len(data)} chars in {(time.time()-start)*1000:.2f}ms")
        return data
    
    def write(self, data: str) -> None:
        start = time.time()
        super().write(data)
        print(f"[LOG] Wrote {len(data)} chars in {(time.time()-start)*1000:.2f}ms")

if __name__ == "__main__":
    storage = FileStorage("test.txt")
    
    enhanced_storage = LoggingWrapper(
        EncryptionWrapper(
            CompressionWrapper(storage),
            key="secret123"
        )
    )
    
    enhanced_storage.write("Hello World! This is sensitive data.")
    print("Reading:", enhanced_storage.read())