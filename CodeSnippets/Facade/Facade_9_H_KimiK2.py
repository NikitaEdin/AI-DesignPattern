import logging
from typing import Optional

class _Logger:
    def __init__(self) -> None:
        self._log = logging.getLogger("sys")
        self._log.setLevel(logging.INFO)
        if not self._log.handlers:
            self._log.addHandler(logging.StreamHandler())

class _Compressor:
    def __init__(self) -> None:
        self._log = _Logger()._log
    def prepare(self, path: str) -> None:
        self._log.info(f"Preparing compressor for {path}")
    def run(self, data: bytes) -> bytes:
        self._log.info("Compressing data")
        return data[::-1]

class _Encryptor:
    def __init__(self) -> None:
        self._log = _Logger()._log
    def prepare(self, key: str) -> None:
        if len(key) < 8:
            raise ValueError("Key too short")
        self._key = key
        self._log.info("Encryptor ready")
    def run(self, data: bytes) -> bytes:
        self._log.info("Encrypting data")
        return bytes(b ^ ord(self._key[i % len(self._key)]) for i, b in enumerate(data))

class _Uploader:
    def __init__(self) -> None:
        self._log = _Logger()._log
    def connect(self, host: str) -> None:
        self._host = host
        self._log.info(f"Connected to {host}")
    def send(self, data: bytes) -> str:
        self._log.info("Uploading...")
        return f"{self._host}/{hash(data) & 0xFFFFFFFF:08x}"

class SecurePipeline:
    def __init__(self) -> None:
        self._compressor = _Compressor()
        self._encryptor = _Encryptor()
        self._uploader = _Uploader()
    def process(self, data: bytes, key: str, host: str) -> Optional[str]:
        try:
            self._compressor.prepare("buffer")
            self._encryptor.prepare(key)
            self._uploader.connect(host)
            compressed = self._compressor.run(data)
            encrypted = self._encryptor.run(compressed)
            return self._uploader.send(encrypted)
        except Exception as e:
            logging.getLogger("sys").error(str(e))
            return None

if __name__ == "__main__":
    pipeline = SecurePipeline()
    result = pipeline.process(b"hello world", "secret123", "s3.example.com")
    print("Uploaded to:", result)