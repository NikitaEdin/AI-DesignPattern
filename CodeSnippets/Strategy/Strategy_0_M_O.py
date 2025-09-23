from abc import ABC, abstractmethod
from typing import List, Tuple
import io
import gzip
import zlib
import sys

class CompressorBase(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass

class GzipCompressor(CompressorBase):
    def compress(self, data: bytes) -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Input must be bytes")
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as f:
            f.write(data)
        return buf.getvalue()

class ZlibCompressor(CompressorBase):
    def compress(self, data: bytes) -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Input must be bytes")
        return zlib.compress(data)

class NoopCompressor(CompressorBase):
    def compress(self, data: bytes) -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Input must be bytes")
        return bytes(data)

class FailingCompressor(CompressorBase):
    def compress(self, data: bytes) -> bytes:
        raise RuntimeError("Intentional failure")

class Compressor:
    def __init__(self, methods: List[CompressorBase]):
        if not methods:
            raise ValueError("At least one compressor required")
        self._methods = methods

    def set_methods(self, methods: List[CompressorBase]):
        if not methods:
            raise ValueError("At least one compressor required")
        self._methods = methods

    def compress(self, data: bytes) -> Tuple[bytes, str]:
        last_error = None
        for method in self._methods:
            try:
                result = method.compress(data)
                return result, method.__class__.__name__
            except Exception as exc:
                last_error = exc
        raise RuntimeError("All compression methods failed") from last_error

if __name__ == "__main__":
    sample = b"The quick brown fox jumps over the lazy dog" * 10
    compressor = Compressor([FailingCompressor(), GzipCompressor(), ZlibCompressor(), NoopCompressor()])
    try:
        compressed, used = compressor.compress(sample)
        print(f"Used: {used}, Compressed size: {len(compressed)} bytes")
    except Exception as e:
        print("Compression failed:", e, file=sys.stderr)

    compressor.set_methods([ZlibCompressor(), NoopCompressor()])
    compressed2, used2 = compressor.compress(sample)
    print(f"Switched to: {used2}, Compressed size: {len(compressed2)} bytes")