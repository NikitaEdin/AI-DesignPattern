import threading
import time

class ResourceManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, connection_string=None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, connection_string=None):
        if getattr(self, "_initialized", False):
            return
        if connection_string is None:
            connection_string = "protocol://localhost"
        self.connection_string = connection_string
        self.connected = False
        self.config = {}
        self._initialized = True

    def configure(self, **settings):
        if not settings:
            raise ValueError("At least one configuration setting is required")
        self.config.update(settings)

    def open_connection(self):
        if self.connected:
            return
        if not self.connection_string:
            raise RuntimeError("Invalid connection string")
        time.sleep(0.05)
        self.connected = True

    def close_connection(self):
        if not self.connected:
            return
        self.connected = False

    def status(self):
        return {
            "instance_id": id(self),
            "connection_string": self.connection_string,
            "connected": self.connected,
            "config": dict(self.config),
        }

def create_and_configure(name, conn_str):
    try:
        rm = ResourceManager(conn_str)
        rm.open_connection()
        rm.configure(thread=name)
        print(f"{name} created instance id:", id(rm))
    except Exception as exc:
        print(f"{name} error:", exc)

if __name__ == "__main__":
    rm1 = ResourceManager("protocol://primary")
    rm1.open_connection()
    rm1.configure(timeout=30, retries=3)
    print("Initial status:", rm1.status())

    rm2 = ResourceManager("protocol://secondary")
    print("Second reference status (should match first):", rm2.status())
    print("rm1 is rm2:", rm1 is rm2)

    try:
        rm1.configure()
    except Exception as e:
        print("Expected configuration error:", e)

    threads = []
    for i in range(5):
        t = threading.Thread(target=create_and_configure, args=(f"worker-{i}", f"protocol://worker-{i}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Final status after threads:", rm1.status())
    rm1.close_connection()
    print("Status after close:", rm1.status())