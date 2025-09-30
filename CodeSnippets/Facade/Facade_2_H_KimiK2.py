import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Optional
import time
import uuid

@dataclass
class DataPacket:
    payload: bytes
    checksum: int
    timestamp: float

class CryptoEngine:
    def __init__(self):
        self._lock = threading.RLock()
    def encrypt(self, data: bytes) -> bytes:
        with self._lock:
            return bytes(b ^ 0x55 for b in data)
    def decrypt(self, data: bytes) -> bytes:
        with self._lock:
            return bytes(b ^ 0x55 for b in data)

class StorageLayer:
    def __init__(self):
        self._store: dict[str, DataPacket] = {}
        self._lock = threading.RLock()
    def write(self, key: str, packet: DataPacket) -> None:
        with self._lock:
            self._store[key] = packet
    def read(self, key: str) -> Optional[DataPacket]:
        with self._lock:
            return self._store.get(key)

class NetworkGateway:
    def __init__(self):
        self._sessions: dict[str, float] = {}
        self._lock = threading.RLock()
    @contextmanager
    def open_session(self, session_id: str):
        with self._lock:
            self._sessions[session_id] = time.time()
        try:
            yield
        finally:
            with self._lock:
                self._sessions.pop(session_id, None)
    def transmit(self, session_id: str, data: bytes) -> None:
        with self._lock:
            if session_id not in self._sessions:
                raise RuntimeError("Invalid session")
            time.sleep(0.001)

class SecureDataExchange:
    def __init__(self):
        self._crypto = CryptoEngine()
        self._storage = StorageLayer()
        self._network = NetworkGateway()
    def send_secure(self, payload: bytes, recipient: str) -> str:
        packet = DataPacket(
            payload=self._crypto.encrypt(payload),
            checksum=sum(payload) & 0xFFFF,
            timestamp=time.time()
        )
        session_id = str(uuid.uuid4())
        with self._network.open_session(session_id):
            self._network.transmit(session_id, packet.payload)
            key = f"{recipient}:{session_id}"
            self._storage.write(key, packet)
        return key
    def receive_secure(self, key: str) -> bytes:
        packet = self._storage.read(key)
        if not packet:
            raise KeyError("No data found")
        payload = self._crypto.decrypt(packet.payload)
        if sum(payload) & 0xFFFF != packet.checksum:
            raise ValueError("Checksum mismatch")
        return payload

if __name__ == "__main__":
    exchange = SecureDataExchange()
    key = exchange.send_secure(b"top secret", "alice")
    print("Sent data with key:", key)
    received = exchange.receive_secure(key)
    print("Received:", received)