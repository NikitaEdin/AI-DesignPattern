import threading
from typing import Dict, Any, Optional
import weakref


class DatabaseManager:
    _instances: Dict[type, Any] = {}
    _lock = threading.RLock()
    _initialized: Dict[int, bool] = {}
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[cls] = instance
                cls._initialized[id(instance)] = False
            return cls._instances[cls]
    
    def __init__(self, host: str = "localhost", port: int = 5432):
        instance_id = id(self)
        if not self._initialized.get(instance_id, False):
            with self._lock:
                if not self._initialized.get(instance_id, False):
                    self.host = host
                    self.port = port
                    self.connections = []
                    self.config = {}
                    self._connection_count = 0
                    self._initialized[instance_id] = True
    
    def connect(self) -> str:
        with self._lock:
            self._connection_count += 1
            connection_id = f"conn_{self._connection_count}"
            self.connections.append(connection_id)
            return connection_id
    
    def disconnect(self, connection_id: str) -> bool:
        with self._lock:
            if connection_id in self.connections:
                self.connections.remove(connection_id)
                return True
            return False
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "host": self.host,
            "port": self.port,
            "active_connections": len(self.connections),
            "total_connections": self._connection_count,
            "instance_id": id(self)
        }
    
    def update_config(self, **kwargs) -> None:
        with self._lock:
            self.config.update(kwargs)
    
    @classmethod
    def reset_instance(cls) -> None:
        with cls._lock:
            if cls in cls._instances:
                instance_id = id(cls._instances[cls])
                del cls._instances[cls]
                cls._initialized.pop(instance_id, None)


class LogManager(DatabaseManager):
    def __init__(self, log_level: str = "INFO", max_size: int = 1000):
        super().__init__()
        instance_id = id(self)
        if not self._initialized.get(instance_id, False):
            with self._lock:
                if not self._initialized.get(instance_id, False):
                    self.log_level = log_level
                    self.max_size = max_size
                    self.logs = []
    
    def log(self, message: str, level: str = "INFO") -> None:
        with self._lock:
            if len(self.logs) >= self.max_size:
                self.logs.pop(0)
            self.logs.append(f"[{level}] {message}")
    
    def get_logs(self) -> list:
        return self.logs.copy()


if __name__ == "__main__":
    def test_thread_safety():
        instances = []
        
        def create_instance():
            db = DatabaseManager("remote-host", 3306)
            instances.append(db)
        
        threads = [threading.Thread(target=create_instance) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        return all(inst is instances[0] for inst in instances)
    
    db1 = DatabaseManager("localhost", 5432)
    db2 = DatabaseManager("different-host", 3306)
    
    print(f"Same instance: {db1 is db2}")
    print(f"DB1 config: {db1.get_status()}")
    print(f"DB2 config: {db2.get_status()}")
    
    conn1 = db1.connect()
    conn2 = db2.connect()
    print(f"Connections after adding: {db1.get_status()['active_connections']}")
    
    logger1 = LogManager("DEBUG", 500)
    logger2 = LogManager("ERROR", 200)
    
    print(f"Same logger instance: {logger1 is logger2}")
    logger1.log("Test message", "DEBUG")
    print(f"Logger2 logs: {len(logger2.get_logs())}")
    
    print(f"Thread safety test passed: {test_thread_safety()}")
    
    DatabaseManager.reset_instance()
    LogManager.reset_instance()
    
    db3 = DatabaseManager("new-host", 8080)
    print(f"New instance after reset: {db1 is db3}")
    print(f"DB3 config: {db3.get_status()}")