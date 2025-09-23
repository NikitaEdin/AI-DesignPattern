import threading
import time
from typing import Optional, Dict, Any

class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None
    _lock = threading.Lock()
    _init_lock = threading.Lock()
    _state_lock = threading.Lock()
    _initialized = False
    
    def __new__(cls) -> 'DatabaseManager':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            with self._init_lock:
                if not self._initialized:
                    self._connection_info = {
                        'host': 'localhost',
                        'port': 5432,
                        'database': 'production',
                        'status': 'disconnected'
                    }
                    self._connections = {}
                    self._transaction_count = 0
                    self._pool_size = 5
                    DatabaseManager._initialized = True
    
    def connect(self, thread_id: str = 'main') -> bool:
        with self._state_lock:
            if thread_id not in self._connections:
                self._connections[thread_id] = {
                    'active': True,
                    'created_at': time.time(),
                    'queries': 0
                }
                self._connection_info['status'] = 'connected'
                return True
            return False
    
    def execute_query(self, query: str, thread_id: str = 'main') -> Dict[str, Any]:
        with self._state_lock:
            if thread_id in self._connections:
                self._connections[thread_id]['queries'] += 1
                self._transaction_count += 1
                return {
                    'success': True,
                    'query': query,
                    'thread_id': thread_id,
                    'total_transactions': self._transaction_count
                }
            return {'success': False, 'error': 'No connection found'}
    
    def get_status(self) -> Dict[str, Any]:
        with self._state_lock:
            return {
                'connection_info': self._connection_info.copy(),
                'active_connections': len(self._connections),
                'total_transactions': self._transaction_count,
                'connections': self._connections.copy()
            }
    
    def disconnect(self, thread_id: str = 'main') -> bool:
        with self._state_lock:
            if thread_id in self._connections:
                del self._connections[thread_id]
                if not self._connections:
                    self._connection_info['status'] = 'disconnected'
                return True
            return False
    
    @classmethod
    def reset_for_testing(cls):
        with cls._lock:
            cls._instance = None
            cls._initialized = False

def worker_function(worker_id: int, results: list):
    manager = DatabaseManager()
    thread_id = f"worker_{worker_id}"
    
    manager.connect(thread_id)
    
    for i in range(3):
        result = manager.execute_query(f"SELECT * FROM table_{i}", thread_id)
        results.append(result)
        time.sleep(0.001)
    
    manager.disconnect(thread_id)

if __name__ == "__main__":
    print("=== Database Manager Test ===")
    
    # Single thread test
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    
    print(f"Same instance: {db1 is db2}")
    
    db1.connect()
    db1.execute_query("CREATE TABLE users")
    db1.execute_query("INSERT INTO users VALUES (1, 'Alice')")
    
    print(f"Status after queries: {db2.get_status()}")
    
    # Multi-threaded test
    print("\n=== Multi-threading Test ===")
    threads = []
    results = []
    
    for i in range(5):
        thread = threading.Thread(target=worker_function, args=(i, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    final_status = db1.get_status()
    print(f"Final transaction count: {final_status['total_transactions']}")
    print(f"Total query results: {len(results)}")
    print(f"Active connections: {final_status['active_connections']}")
    
    # Verify instance consistency across threads
    test_manager = DatabaseManager()
    print(f"Instance consistent after threading: {test_manager is db1}")