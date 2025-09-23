from abc import ABC, abstractmethod
from typing import Dict, Callable, Any

class Connection(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass

class MySQLConnection(Connection):
    def __init__(self, host: str = 'localhost', user: str = 'root', password: str = ''):
        self.host = host
        self.user = user
        self.password = password

    def connect(self) -> str:
        return f"Connected to MySQL at {self.host} as {self.user}"

class PostgreSQLConnection(Connection):
    def __init__(self, host: str = 'localhost', user: str = 'postgres', password: str = ''):
        self.host = host
        self.user = user
        self.password = password

    def connect(self) -> str:
        return f"Connected to PostgreSQL at {self.host} as {self.user}"

class ConnectionRegistry:
    _creators: Dict[str, Callable[..., Connection]] = {}

    @classmethod
    def register(cls, type_name: str, creator: Callable[..., Connection]) -> None:
        if type_name in cls._creators:
            raise ValueError(f"Type {type_name} already registered")
        cls._creators[type_name] = creator

    @classmethod
    def unregister(cls, type_name: str) -> None:
        cls._creators.pop(type_name, None)

    @classmethod
    def is_registered(cls, type_name: str) -> bool:
        return type_name in cls._creators

    @classmethod
    def get_creator(cls, type_name: str) -> Callable[..., Connection] | None:
        return cls._creators.get(type_name)

class DatabaseManager:
    def __init__(self):
        self.registry = ConnectionRegistry

    def create_connection(self, db_type: str, **kwargs: Any) -> Connection:
        if not self.registry.is_registered(db_type):
            raise ValueError(f"Unsupported database type: {db_type}")
        
        creator = self.registry.get_creator(db_type)
        if creator is None:
            raise ValueError(f"Creator not found for type: {db_type}")
        
        # Validate required parameters based on type
        if db_type == "mysql" and "host" not in kwargs:
            kwargs["host"] = "default_mysql_host"
        elif db_type == "postgresql" and "host" not in kwargs:
            kwargs["host"] = "default_pg_host"
        
        try:
            return creator(**kwargs)
        except TypeError as e:
            raise ValueError(f"Invalid parameters for {db_type}: {e}")

# Initialize registry
ConnectionRegistry.register("mysql", MySQLConnection)
ConnectionRegistry.register("postgresql", PostgreSQLConnection)

if __name__ == "__main__":
    manager = DatabaseManager()
    
    # Successful creations
    conn1 = manager.create_connection("mysql", host="mysql.example.com", user="admin", password="secret")
    print(conn1.connect())
    
    conn2 = manager.create_connection("postgresql", user="pguser")
    print(conn2.connect())
    
    # Error handling
    try:
        conn3 = manager.create_connection("oracle")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Demonstrate registration check
    print(f"MySQL registered: {manager.registry.is_registered('mysql')}")
    
    # Unregister and check
    manager.registry.unregister("mysql")
    print(f"MySQL registered after unregister: {manager.registry.is_registered('mysql')}")
    
    try:
        manager.create_connection("mysql")
    except ValueError as e:
        print(f"Error after unregister: {e}")